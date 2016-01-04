#
# Collective Knowledge (program optimization)
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
# test remote access

def test(i):
    """
    Input:  {
              (email)      - optional email
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              status       - string with status
            }

    """

    import os

    o=i.get('out','')

    status="CK server works fine!";

    email=i.get('email','')

    r=ck.get_current_date_time({})
    if r['return']>0: return r

    s=r['iso_datetime']

    if email!='': s+='; '+email

    # Prepare logging
    r=get_path({})
    if r['return']>0: return r

    px=r['path']

    path=os.path.join(px, cfg['log_file_test'])

    try:
       with open(path, "a") as f:
          f.write(s+'\n')
       f.close()
    except Exception as e: 
       return {'return':1, 'error':'problem logging ('+format(e)+')'}

    if o=='con':
       ck.out(status)

    return {'return':0, 'status':status}

##############################################################################
# get path to internal/local/tmp crowdsourcing files

def get_path(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    import os

    rps=os.environ.get(cfg['env_key_crowdsource_path'],'').strip()
    if rps=='': 
       # Get home user directory
       from os.path import expanduser
       home = expanduser("~")

       # In the original version, if path to repos was not defined, I was using CK path,
       # however, when installed as root, it will fail
       # rps=os.path.join(work['env_root'],cfg['subdir_default_repos'])
       # hence I changed to <user home dir>/CK
       rps=os.path.join(home, cfg['crowdsource_path'])

    if not os.path.isdir(rps):
       os.makedirs(rps)

    return {'return':0, 'path':rps}

##############################################################################
# crowdsource program optimization

def crowdsource(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    print ('crowdsource program optimization')

    ck.out('')
    ck.out('Command line: ')
    ck.out('')

    import json
    cmd=json.dumps(i, indent=2)

    ck.out(cmd)

    return {'return':0}

##############################################################################
# explore program optimizations

def explore(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """

    print ('explore program optimizations')

    ck.out('')
    ck.out('Command line: ')
    ck.out('')

    import json
    cmd=json.dumps(i, indent=2)

    ck.out(cmd)

    return {'return':0}

##############################################################################
# generate experiment pack for crowdsourcing in remote hardware (mobile phones or tablets)

def generate_for_remote(i):
    """
    Input:  {
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """


    import os

    p=os.path.join(work['path'],'ck-crowdsource-experiment-pack.zip')

    if not os.path.isfile(p):
       return {'return':1, 'error':'experiment pack file not found'}

    size=os.path.getsize(p) 

    r=ck.convert_file_to_upload_string({'filename':p})
    if r['return']>0: return r

    fx=r['file_content_base64']

    #MD5
    import hashlib
    md5=hashlib.md5(fx.encode()).hexdigest()

    print fx

    return {'return':0, 'file_content_base64':fx, 'size':size, 'md5sum':md5}