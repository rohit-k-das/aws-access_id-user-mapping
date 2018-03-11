import boto3
import os

#Get user name for access id
def access_keys(profile,accesskeyid):
    session = boto3.session.Session(profile_name = profile)
    client = session.client('iam')
    userlist = client.list_users()
    for user in userlist['Users']:
        username = user['UserName']
        keylist = client.list_access_keys(UserName=username)
        for key in keylist['AccessKeyMetadata']:
            key_ID = key['AccessKeyId']
            if accesskeyid == key_ID:
                print "Access id belongs to user " + key['UserName'] + " in profile " + profile
                exit(0)

#Get all AWS account profiles from aws credentials file
def get_profiles(cred_file):
    profiles = []
    try:
        with open(cred_file) as f:
            for line in f.readlines():
                if '[' in line:
                    line = line.replace('[','').replace(']','').strip('\n')
                    profiles.append(line)
    except Exception,e:
        print "Error:" +str(e)
    return profiles

#Get default home dir of user executing the script
def get_home_dir():
    current_user_id = os.getuid()
    with  open('/etc/passwd') as passwd_file:
        for line in passwd_file.readlines():
            field = line.split(':')
            if current_user_id == int(field[2]):
                home_dir = field[5]
    return home_dir

def main():
    home_dir = get_home_dir()
    cred_file_path = home_dir + '/.aws/credentials'

    #Checks if aws credential file exists and get all AWS account profiles
    if os.path.exists(cred_file_path):
        profiles = get_profiles(cred_file_path)
    else:
        cred_file_path = raw_input("Please enter credential files absolute path: ")
        profiles = get_profiles(cred_file_path)

    #Access ID to be searched
    accesskeyid = raw_input("Enter Access ID: ")
    accesskeyid = accesskeyid.strip('\n').strip('\r')
    print "Scanning profiles " + str(profiles) + " for access id " + accesskeyid + ' ...\n'

    for profile in profiles:
        try:
            access_keys(profile, accesskeyid)
        except Exception,e:
            print 'ERROR: Lack of permissions to access AWS IAM for account ' + profile + ' .'

if __name__ == '__main__':
    main()

