#
# Collective Knowledge: compiler flags crowdtuning (crowdsource autotuning via spare computers such as mobile devices)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings
compiler_choices='#choices#compiler_flags#'

line='================================================================'

fsummary='summary.json'
fclassification='classification.json'
fgraph='tmp-reactions-graph.json'

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# show results

def html_viewer(i):
    """      
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              html
              (style)      - styles - useful for plotting JavaScript-based graphs
            }

    """

    import os
    global cfg, work

    orig_module_uid=work['self_module_uid']

    mcfg=i.get('module_cfg',{})
    if len(mcfg)>0: cfg=mcfg

    mwork=i.get('module_work',{})
    if len(mwork)>0: work=mwork

    st=''

    url0=i['url_base']

    ap=i.get('all_params',{})

    ruoa=i.get('repo_uoa','')
    muoa=work['self_module_uoa']
    muid=work['self_module_uid']
    duoa=i.get('data_uoa','')

    ik=cfg['improvements_keys']

    # Load program optimization entry
    rx=ck.access({'action':'load',
                  'module_uoa':cfg['module_deps']['module'],
                  'data_uoa':cfg['module_deps']['program.optimization']})
    if rx['return']>0: return rx
    urld=rx['dict'].get('url_discuss','')

    # Load Entry
    r=ck.access({'action':'load',
                 'repo_uoa':ruoa,
                 'module_uoa':muoa,
                 'data_uoa':duoa})
    if r['return']>0: 
       return {'return':0, 'html':'<b>CK error:</b> '+r['error']+'!'}

    p=r['path']
    d=r['dict']
    duid=r['data_uid']

    # Load program module to get desc keys
    r=ck.access({'action':'load',
                 'module_uoa':cfg['module_deps']['module'],
                 'data_uoa':cfg['replay_desc']['module_uoa']})
    if r['return']>0: return r
    pdesc=r.get('desc',{})
    xxkey=cfg['replay_desc'].get('desc_key','')
    if xxkey!='':
       pdesc=pdesc.get(xxkey,{})

    h='<center>\n'
    h+='\n\n<script language="JavaScript">function copyToClipboard (text) {window.prompt ("Copy to clipboard: Ctrl+C, Enter", text);}</script>\n\n' 

    h+='<H2>Distinct solutions after online classification ('+cfg['desc']+')</H2>\n'
    h+='</center>\n'

    h+='<p>\n'

    cid=muid+':'+duid

    h+='<table border="0" cellpadding="4" cellspacing="0">\n'
    x=muid
    if muoa!=muid: x+=' ('+muoa+')'
    h+='<tr><td><b>Scenario UID</b></td><td>'+x+'</td></tr>\n'
    h+='<tr><td><b>Data UID</b></td><td>'+duid+'</td></tr>\n'
    h+='<tr><td><td></td></tr>\n'

    url5=ck.cfg.get('wiki_data_web','')

    if url5!='' or urld!='':
       if url5!='':
          x='<a href="'+url5+muid+'_'+duid+'">GitHub wiki</a>'
       if urld!='':
          if x!='': x+=', '
          x+='<a href="'+urld+'">Google group</a>' 

       h+='<tr><td><b>Discuss:</b></td><td>'+x+'</td></tr>\n'

       h+='<tr><td><td></td></tr>\n'

    urlx=url0+'action=get&cid='+cfg['module_deps']['program.optimization']+':'+duid+'&scenario_module_uoa='+muid+'&out=json'
    urls=url0+'action=pull&common_action=yes&cid='+muid+':'+duid+'&filename=summary.json'
    urlc=url0+'action=pull&common_action=yes&cid='+muid+':'+duid+'&filename=classification.json'

    x=''
    if urls!='':
       x+='[ <a href="'+urls+'">All solutions in JSON</a> ]'
    if urlc!='':
       if x!='': x+=', '
       x+='[ <a href="'+urlc+'">Solutions\' classification in JSON</a> ]'

    if x!='':
       h+='<tr><td><b>Download:</b></td><td>'+x+'</td></tr>\n'

    h+='<tr><td><b>Reproduce all (with reactions):</b></td><td><i>ck replay '+cid+'</i></td></tr>\n'

    h+='<tr><td><td></td></tr>\n'

    pr=cfg.get('prune_results',[])
    mm=d.get('meta',{})
    em=d.get('extra_meta',{})
    obj=mm.get('objective','')

    for k in pr:
        qd=k.get('desc','')
        qi=k.get('id','')
        qr=k.get('ref_uid','')
        qm=k.get('ref_module_uoa','')

        x=mm.get(qi,'')
        if x!='' and qm!='' and qr!='':
           xuid=mm.get(qr,'')
           if xuid!='':
              x='<a href="'+url0+'wcid='+qm+':'+xuid+'">'+x+'</a>'

        h+='<tr><td><b>'+qd+'</b></td><td>'+x+'</td></tr>\n'

    h+='<tr><td><b>Objective</b></td><td>'+obj+'</td></tr>\n'

    h+='<tr><td></td><td></td></tr>\n'

    kk=0
    for kx in range(0, len(ik)):
        k=ik[kx]
        k1=k.replace('$#obj#$',obj)
        ik[kx]=k1

        if pdesc.get(k1,{}).get('desc','')!='':
           k1=pdesc[k1]['desc']

        kk+=1

        h+='<tr><td><b>Improvement key IK'+str(kk)+'</b></td><td>'+k1+'</td></tr>\n'

    ik0=ik[0] # first key to sort

    h+='</table>\n'

    h+='<p>\n'
    h+='<center>\n'

    bgraph={"0":[], "1":[]} # graph with highest improvements

    # Load summary
    sols=[]

    psum=os.path.join(p, fsummary)
    if os.path.isfile(psum):
       rx=ck.load_json_file({'json_file':psum})
       if rx['return']>0: return rx
       sols=rx['dict']

    # Load classification file
    classification={}
    pcl=os.path.join(p, fclassification)
    if os.path.isfile(pcl):
       rx=ck.load_json_file({'json_file':pcl})
       if rx['return']>0: return rx
       classification=rx['dict']

    h+='<p>\n'
    h+='$#graph#$\n'
    h+='<p>\n'

    # List solutions
    if len(sols)==0:
       h+='<h2>No distinct solutions found!</h2>\n'
    else:
       # Check host URL prefix and default module/action
       h+='<table class="ck_table" border="0">\n'

       h+=' <tr style="background-color:#cfcfff;">\n'
       h+='  <td colspan="1"></td>\n'
       h+='  <td colspan="1" style="background-color:#bfbfff;"></td>\n'
       h+='  <td colspan="'+str(len(ik))+'" align="center"><b>Improvements (<4% variation)</b></td>\n'
       h+='  <td colspan="2" align="center" style="background-color:#bfbfff;"></td>\n'
       h+='  <td colspan="4"></td>\n'
       h+='  <td colspan="4" align="center" style="background-color:#bfbfff;"><b>Distinct workload for highest improvement</b></td>\n'
       h+='  <td colspan="4"></td>\n'
       h+='  <td colspan="1" align="center" style="background-color:#bfbfff;"></td>\n'
       h+=' </tr>\n'

       h+=' <tr style="background-color:#cfcfff;">\n'
       h+='  <td><b>\n'
       h+='   #\n'
       h+='  </b></td>\n'
       h+='  <td style="background-color:#bfbfff;"><b>\n'
       h+='   Solution UID\n'
       h+='  </b></td>\n'

       for k in range(0, len(ik)):
           h+='  <td align="right"><b>\n'
           h+='   IK'+str(k+1)+'\n'
           h+='  </b></td>\n'

       h+='  <td align="center" style="background-color:#bfbfff;"><b>\n'
       h+='   New distinct optimization choices\n'
       h+='  </b></td>\n'
       h+='  <td align="center" style="background-color:#bfbfff;" align="right"><b>\n'
       h+='   Ref\n'
       h+='  </b></td>\n'

       h+='  <td align="center"><b>\n'
       h+='   Best species\n'
       h+='  </b></td>\n'
       h+='  <td align="center"><b>\n'
       h+='   Worst species\n'
       h+='  </b></td>\n'
       h+='  <td align="center"><b>\n'
       h+='   Touched\n'
       h+='  </b></td>\n'
       h+='  <td align="center"><b>\n'
       h+='   Iters\n'
       h+='  </b></td>\n'
       h+='  <td style="background-color:#bfbfff;"><b>\n'
       h+='   Program\n'
       h+='  </b></td>\n'
       h+='  <td style="background-color:#bfbfff;"><b>\n'
       h+='   CMD\n'
       h+='  </b></td>\n'
       h+='  <td style="background-color:#bfbfff;"><b>\n'
       h+='   Dataset\n'
       h+='  </b></td>\n'
       h+='  <td style="background-color:#bfbfff;"><b>\n'
       h+='   Dataset file\n'
       h+='  </b></td>\n'
       h+='  <td align="right"><b>\n'
       h+='   CPU freq (MHz)\n'
       h+='  </b></td>\n'
       h+='  <td align="right"><b>\n'
       h+='   Cores\n'
       h+='  </b></td>\n'
       h+='  <td><b>\n'
       h+='   Platform\n'
       h+='  </b></td>\n'
       h+='  <td><b>\n'
       h+='   OS\n'
       h+='  </b></td>\n'

       h+='  <td align="center" style="background-color:#bfbfff;">\n'
       h+='   <b>Replay</b>\n'
       h+='  </td>\n'

       h+=' </tr>\n'

       # List
       num=0
       iq=-1
       iq1=0

       res={}
       sres=[]
       ires=0

       em={}

       cls={}

       while iq1<len(sols): # already sorted by most "interesting" solutions (such as highest speedups)
           if iq!=iq1:
              num+=1

              iq+=1
              q=sols[iq]

              em=q.get('extra_meta',{})

              suid=q['solution_uid']

              cls=classification.get(suid,{})

              xcls=cls.get('highest_improvements_workload',{})
              program_uoa=xcls.get('program_uoa','')
              cmd=xcls.get('cmd_key','')
              dataset_uoa=xcls.get('dataset_uoa','')
              dataset_file=xcls.get('dataset_file','')

              wl_best=len(cls.get('best',[]))
              wl_worst=len(cls.get('worst',[]))

              url_wl=url0+'action=get_workloads&cid='+cfg['module_deps']['program.optimization']+':'+duid+'&scenario_module_uoa='+muid+'&solution_uid='+suid+'&out=json'
              url_wl_best=url_wl+'&key=best'
              url_wl_worst=url_wl+'&key=worst'

              res={}
              ref_res={}
              sres=[]
              ires=0

              # Try to load all solutions
              p1=os.path.join(p, suid)

              try:
                 dirList=os.listdir(p1)
              except Exception as e:
                  None
              else:
                  for fn in dirList:
                      if fn.startswith('ckp-') and fn.endswith('.flat.json'):
                         uid=fn[4:-10]

                         px=os.path.join(p1, fn)
                         rx=ck.load_json_file({'json_file':px})
                         if rx['return']>0: return rx
                         d1=rx['dict']

                         px=os.path.join(p1,'ckp-'+uid+'.features_flat.json')
                         if rx['return']>0: return rx
                         d2=rx['dict']

                         x={'flat':d1, 'features_flat':d2}

                         px=os.path.join(p1, 'ckp-'+uid+'.features.json')
                         rx=ck.load_json_file({'json_file':px})
                         if rx['return']>0: return rx
                         dx=rx['dict']

                         if dx.get('permanent','')=='yes':
                            ref_res==x
                         else:
                            res[uid]=x
                         
                  rr=list(res.keys())
                  sres=sorted(rr, key=lambda v: (float(res[v].get('flat',{}).get(ik0,0.0))), reverse=True)

           rr={}
           if ires<len(sres):
              rr=res.get(sres[ires],{})
              ires+=1

              iterations=q.get('iterations',1)
              touched=q.get('touched',1)

              choices=q['choices']

              ref_sol=q.get('ref_choices',{})
              ref_sol_order=q.get('ref_choices_order',[])

              target_os=choices.get('target_os','')

              speedup=''

              cmd1=''
              cmd2=''

              ss='S'+str(num)
              h+=' <tr>\n'
              h+='  <td valign="top" style="background-color:#efefff;">\n'
              if ires<2:

                 h+='   '+ss+'\n'
              h+='  </td>\n'

              h+='  <td valign="top">\n'
              if ires<2 and urlx!='':
                 h+='   <a href="'+urlx+'&solution_uid='+suid+'">'+suid+'</a>\n'
              h+='  </td>\n'

              for k in range(0, len(ik)):
                  h+='  <td valign="top" align="right" style="background-color:#efefff;">\n'

#                  dv=rr.get('flat',{}).get(ik[k],'')

                  dv=''
                  dvw=''
                  points=q.get('points',[])
                  iresx=ires-1
#                  if iresx<len(points):
#                     dv=points[iresx].get('improvements_best',{}).get(ik[k],'')
#                     dvw=points[iresx].get('improvements_worst',{}).get(ik[k],'')

                  # Add to graph (first dimension and first solution)
#                  if k==0 and ires==1:
                  dv=cls.get('highest_improvements',{}).get(ik[k],'')
                  dvw=cls.get('highest_degradations',{}).get(ik[k],'')

                  if k==0:
                     bgraph['0'].append([ss,dv])
                     bgraph['1'].append([ss,dvw])

                  y=''
                  if type(dv)==int or type(dv)==ck.type_long:
                     y=str(dv)
                  else:
                     try:
                        y=('%.2f' % dv)
                     except Exception as e: 
                        y=dv
                        pass

                  if dv!='':
                     if dv>1.0:
                        y='<span style="color:#bf0000">'+y+'</span>'
                     elif dv!=0:
                        y='<span style="color:#0000bf">'+y+'</span>'
                  

                  h+=str(y)+'\n'
                  h+='  </td>\n'


              h+='  <td valign="top">\n'
              dv=rr.get('flat',{}).get('##characteristics#compile#joined_compiler_flags#min','')
              h+='   '+dv+'\n'
              h+='  </td>\n'

              h+='  <td valign="top" align="center">\n'
              if ires<2:
                 # Ideally should add pipeline description somewhere
                 # to properly recreate flags. However since it is most of the time -Ox
                 # we don't need to make it complex at the moment 

                 ry=rebuild_cmd({'choices':ref_sol,
                                 'choices_order':ref_sol_order,
                                 'choices_desc':{}})
                 if ry['return']>0: return ry
                 ref=ry['cmd']

                 h+='   '+ref+'\n'
              h+='   \n'
              h+='  </td>\n'

              h+='  <td valign="top" align="center" style="background-color:#efefff;">\n'
              if ires<2:
                 h+='   <a href="'+url_wl_best+'">'+str(wl_best)+'</a>\n'
              h+='  </td>\n'

              h+='  <td valign="top" align="center" style="background-color:#efefff;">\n'
              if ires<2:
                 h+='   <a href="'+url_wl_worst+'">'+str(wl_worst)+'</a>\n'
              h+='  </td>\n'

              h+='  <td valign="top" align="center" style="background-color:#efefff;">\n'
              if ires<2:
                 h+='   '+str(touched)+'\n'
              h+='  </td>\n'

              h+='  <td valign="top" align="center" style="background-color:#efefff;">\n'
              if ires<2:
                 h+='   '+str(iterations)+'\n'
              h+='  </td>\n'

              h+='  <td valign="top">\n'
              if ires<2:
                 h+='   <a href="'+url0+'wcid=program:'+program_uoa+'">'+program_uoa+'</a>\n'
              h+='  </td>\n'

              h+='  <td valign="top">\n'
              if ires<2:
                 h+='   '+cmd+'\n'
              h+='  </td>\n'

              h+='  <td valign="top">\n'
              if ires<2:
                 h+='   <a href="'+url0+'wcid=dataset:'+dataset_uoa+'">'+dataset_uoa+'</a>\n'
              h+='  </td>\n'

              h+='  <td valign="top">\n'
              if ires<2:
                 h+='   <a href="'+url0+'action=pull&common_func=yes&cid=dataset:'+dataset_uoa+'&filename='+dataset_file+'">'+dataset_file+'</a>\n'
              h+='  </td>\n'

#              h+='  <td valign="top" align="right">\n'
#              if ires<2:
#                 h+='   '+str(em.get('kernel_repetitions',-1))+'\n'
#              h+='  </td>\n'

              h+='  <td valign="top" align="right" style="background-color:#efefff;">\n'
              if ires<2:
                 x=''
                 qq=em.get('cpu_cur_freq',[])
                 for q in qq:
                     xq=qq[q]
                     if x!='': x+=', '
                     x+=str(xq)
                 h+='   '+x+'\n'
              h+='  </td>\n'

              h+='  <td valign="top" align="right" style="background-color:#efefff;">\n'
              if ires<2:
                 qq=em.get('cpu_num_proc',1)
                 h+='   '+str(qq)+'\n'
              h+='  </td>\n'

              h+='  <td valign="top" style="background-color:#efefff;">\n'
              if ires<2:
                 h+='   '+str(em.get('platform_name',''))+'\n'
              h+='  </td>\n'

              h+='  <td valign="top" style="background-color:#efefff;">\n'
              if ires<2:
                 h+='   '+str(em.get('os_name',''))+'\n'
              h+='  </td>\n'

              x='ck replay '+cid+' --solution_uid='+suid
              y=ck.cfg.get('add_extra_to_replay','')
              if y!='':x+=' '+y
              h+='    <td valign="top" align="center"><input type="button" class="ck_small_button" style="height:60px;" onClick="copyToClipboard(\''+x+'\');" value="Copy \nto \nclipboard"></td>\n'

              h+=' </tr>\n'

           else:
              iq1+=1


       h+='</table>\n'
       h+='<br><a href="http://arxiv.org/abs/1506.06256"><img src="'+url0+'action=pull&common_action=yes&cid='+cfg['module_deps']['module']+':'+orig_module_uid+'&filename=images/image-workflow1.png"></a>\n'

    h+='</center>\n'

    h+='<br><br>\n'

    rx=ck.access({'action':'links',
                  'module_uoa':cfg['module_deps']['program.optimization']})
    if rx['return']>0: return rx
    h+=rx['html']

    # Plot graph
    hg=''
    ftmp=''

    if len(bgraph['0'])>0:
       ii={'action':'plot',
           'module_uoa':cfg['module_deps']['graph'],

           "table":bgraph,

           "h_lines":[1.0],

           "ymin":0,

           "ignore_point_if_none":"yes",

           "plot_type":"d3_2d_bars",

           "display_y_error_bar":"no",

           "title":"Powered by Collective Knowledge",

           "axis_x_desc":"Distinct optimization solutions (highest improvement vs highest degradation)",
           "axis_y_desc":"Max improvement ( IK1 = Ref / Solution )",

           "plot_grid":"yes",

           "d3_div":"ck_interactive",

           "image_width":"900",
           "image_height":"400",

           "wfe_url":url0}

       # Trick to save to file (for interactive/live articles)
       if ap.get('fgg_save_graph_to_file','')=='yes':
          import copy
          iii=copy.deepcopy(ii)
          iii["substitute_x_with_loop"]="yes"
          iii["plot_type"]="mpl_2d_bars" 
          if 'ymin' in iii: del(iii['ymin'])
          if 'ymax' in iii: del(iii['ymax'])

          # Prepare batch file
          rx=ck.gen_tmp_file({'prefix':'tmp-', 'suffix':'.json'})
          if rx['return']>0: return rx
          ftmp=rx['file_name']

          rx=ck.save_json_to_file({'json_file':ftmp, 'dict':iii, 'sort_keys':'yes'})
          if rx['return']>0: return rx

       r=ck.access(ii)
       if r['return']==0:
          x=r.get('html','')
          if x!='':
             st=r.get('style','')

             hg='<div id="ck_box_with_shadow" style="width:920px;">\n'
             if ftmp!='':
                hg+='<center><b>Note: graph info has been saved to file '+ftmp+' for interactive publications</b></center>'
             hg+=' <div id="ck_interactive" style="text-align:center">\n'
             hg+=x+'\n'
             hg+=' </div>\n'
             hg+='</div>\n'

    h=h.replace('$#graph#$', hg)

    return {'return':0, 'html':h, 'style':st}

##############################################################################
# crowdsource these experiments

def crowdsource(i):
    """
    Input:  {
              See 'crowdsource program.optimization'

              (compiler_env_uoa)           - fix compiler environment
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    global cfg, work

    import copy

    mcfg=i.get('module_cfg',{})
    if len(mcfg)>0: 
       cfg=mcfg

    mwork=i.get('module_work',{})
    if len(mwork)>0: work=mwork

    # Setting output
    o=i.get('out','')
    oo=''
    if o=='con': oo='con'

    quiet=i.get('quiet','')

    er=i.get('exchange_repo','')
    if er=='': er=ck.cfg['default_exchange_repo_uoa']
    esr=i.get('exchange_subrepo','')
    if esr=='': esr=ck.cfg['default_exchange_subrepo_uoa']

    if i.get('local','')=='yes': 
       er='local'
       esr=''

    la=i.get('local_autotuning','')

    # Get user 
    user=''

    mcfg={}
    ii={'action':'load',
        'module_uoa':'module',
        'data_uoa':cfg['module_deps']['program.optimization']}
    r=ck.access(ii)
    if r['return']==0:
       mcfg=r['dict']

       dcfg={}
       ii={'action':'load',
           'module_uoa':mcfg['module_deps']['cfg'],
           'data_uoa':mcfg['cfg_uoa']}
       r=ck.access(ii)
       if r['return']>0 and r['return']!=16: return r
       if r['return']!=16:
          dcfg=r['dict']

       user=dcfg.get('user_email','')

    ceuoa=i.get('compiler_env_uoa', '')

    if ceuoa!='':
       rx=ck.access({'action':'load',
                     'module_uoa':cfg['module_deps']['env'],
                     'data_uoa':ceuoa})
       if rx['return']>0: return rx
       ceuoa=rx['data_uid']

    # Initialize local environment for program optimization ***********************************************************
    pi=i.get('platform_info',{})
    if len(pi)==0:
       ii=copy.deepcopy(i)
       ii['action']='initialize'
       ii['module_uoa']=cfg['module_deps']['program.optimization']
       ii['exchange_repo']=er
       ii['exchange_subrepo']=esr
       r=ck.access(ii)
       if r['return']>0: return r

       pi=r['platform_info']
       user=r.get('user','')

    hos=pi['host_os_uoa']
    hosd=pi['host_os_dict']

    tos=pi['os_uoa']
    tosd=pi['os_dict']
    tbits=tosd.get('bits','')

    remote=tosd.get('remote','')

    tdid=pi['device_id']

    program_tags=i.get('program_tags','')
    if program_tags=='' and i.get('local_autotuning','')!='yes' and i.get('data_uoa','')=='':
       program_tags=cfg['program_tags']

    # Check that has minimal dependencies for this scenario ***********************************************************
    sdeps=i.get('dependencies',{}) # useful to preset inside crowd-tuning
    if len(sdeps)==0:
       sdeps=copy.deepcopy(cfg['deps'])
    if len(sdeps)>0:
       if o=='con':
          ck.out(line)
          ck.out('Resolving software dependencies required for this scenario ...')
          ck.out('')

       if ceuoa!='':
          x=sdeps.get('compiler',{})
          if len(x)>0:
             if 'cus' in x: del(x['cus'])
             if 'deps' in x: del(x['deps'])
             x['uoa']=ceuoa
             sdeps['compiler']=x

       ii={'action':'resolve',
           'module_uoa':cfg['module_deps']['env'],
           'host_os':hos,
           'target_os':tos,
           'device_id':tdid,
           'deps':sdeps,
           'add_customize':'yes'}
       if quiet=='yes': 
          ii['random']='yes'
       else:
          ii['out']=oo
       rx=ck.access(ii)
       if rx['return']>0: return rx

       sdeps=rx['deps'] # Update deps (add UOA)

    cpu_name=pi.get('features',{}).get('cpu',{}).get('name','')
    compiler_soft_uoa=sdeps.get('compiler',{}).get('dict',{}).get('soft_uoa','')
    compiler_env=sdeps.get('compiler',{}).get('bat','')

    plat_extra={}
    pft=pi.get('features',{})
    for q in pft:
        if q.endswith('_uid'):
           plat_extra[q]=pft[q]
        elif type(pft[q])==dict and pft[q].get('name','')!='':
           plat_extra[q+'_name']=pft[q]['name']

    # Detect real compiler version ***********************************************************
    if o=='con':
       ck.out(line)
       ck.out('Detecting compiler version ...')

    ii={'action':'internal_detect',
        'module_uoa':cfg['module_deps']['soft'],
        'data_uoa':compiler_soft_uoa,
        'host_os':hos,
        'target_os':tos,
        'target_device_id':tdid,
        'env':compiler_env}
    r=ck.access(ii)
    if r['return']>0: return r

    compiler_version=r['version_str']

    compiler=cfg.get('compiler_name','')+' '+compiler_version

    if o=='con':
       ck.out('')
       ck.out('* Compiler: '+compiler)
       ck.out('* CPU:      '+cpu_name)

    # Start preparing input to run program.optimization
    ii=copy.deepcopy(i)

    ii['action']='run'
    ii['module_uoa']=cfg['module_deps']['program.optimization']

    ii['host_os']=hos
    ii['target_os']=tos
    ii['target_device_id']=tdid
    ii['dependencies']=sdeps

    ii['scenario_cfg']=cfg

    ii['platform_info']=pi

    ii['program_tags']=program_tags

    ii['scenario_module_uoa']=work['self_module_uid']

    ii['experiment_meta']={'cpu_name':cpu_name,
                           'compiler':compiler}

    ii['experiment_meta_extra']=plat_extra

    ii['exchange_repo']=er
    ii['exchange_subrepo']=esr

    ii['user']=user

    # Select sub-scenario ********************************************************************
    from random import randint
    ss=1 # num of scenarios

    sx=randint(1,ss)

    rr={'return':0}

    if sx==1 or la=='yes':
       # **************************************************************** explore random program/dataset
       sdesc='explore random program/cmd/data set'
       if o=='con':
          ck.out('')
          ck.out('  ****** Sub-scenario: '+sdesc+' ******')

       ii['subscenario_desc']=sdesc

       rr=ck.access(ii)
       if rr['return']>0: return rr

    rr['platform_info']=pi

    return rr

##############################################################################
# rebuild compiler cmd from choices

def rebuild_cmd(i):
    """
    Input:  {
               choices       - dict of choices
               choices_order - choices order
               choices_desc  - dict of choices desc
            }

    Output: {
              return         - return code =  0, if successful
                                           >  0, if error
              (error)        - error text if return > 0

              cmd            - compiler command line
              pruned_choices - leave only compiler flags
            }

    """

    cmd=''

    choices=i.get('choices',{})
    corder=i.get('choices_order',[])
    cdesc=i.get('choices_desc',{})

    for q in sorted(corder):
        v=choices.get(q, None)
        d=cdesc.get(q, None)

        if v!=None:
           if cmd!='': cmd+=' '
           cmd+=v

    return {'return':0, 'cmd':cmd}
