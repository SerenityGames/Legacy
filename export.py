#!/usr/bin/env python3

import yaml
import datetime
from slugify import Slugify
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb as mysql
import getpass

def clean_rank(rank):
    if 'REGISTERED' in rank or 'NEWLY_REGISTERED' in rank:
        rank = 'Builder'
    if 'GLOBAL_MODERATORS' in rank:
        rank = 'Moderator'
    if 'Serenitybot' in rank:
        rank = 'Bot'
    rank = rank.capitalize()
    rank = rank.strip('s')
    return rank

slugify = Slugify(to_lower=True)

db_username = raw_input("Username:")
db_password = getpass.getpass('Password: ')

cnx = mysql.connect(user=db_username, password=db_password, database='Serenity_Forum')
mcursor = cnx.cursor()

mquery = ("select phpbb_users.user_id as uid, username, pf_minecraft_ign as ign, phpbb_groups.group_name as primary_group from phpbb_users LEFT JOIN phpbb_profile_fields_data ON phpbb_users.user_id = phpbb_profile_fields_data.user_id LEFT JOIN phpbb_groups ON phpbb_users.group_id = phpbb_groups.group_id WHERE user_posts > 0 AND user_type != 2 GROUP BY ign ")

mcursor.execute(mquery)

#Get users
for (uid, username, ign, primary_rank) in mcursor:
    cursor = cnx.cursor()
    username.replace(" ", "_")
    #You are a funny guy. Shoo!
    if ign == "Serenity Games":
        continue
    #Get rid of email addresses as usernames
    if "@" in username:
        continue
    if ign:
        #IGN's shouldn't have spaces
        ign.replace(" ", "_")
        #IGN's shouldn't be emails
        if "@" in ign:
            continue
        #One user has a "/" in the IGN field. We will prefer the first name.
        ign = ign.split("/")[0]
        #Silly Rainbow... We gonna use your forum username
        if not "(Blues)" in ign:
            #If IGN exists, use that!
            username = ign
    #Get user's ranks
    query = ("select group_name from phpbb_groups LEFT JOIN phpbb_user_group ON phpbb_groups.group_id = phpbb_user_group.group_id LEFT JOIN phpbb_users ON phpbb_users.user_id = phpbb_user_group.user_id WHERE phpbb_users.user_id = %s")
    cursor.execute(query, (uid))
    ranks = ()
    #Create a list of ranks. Clean them up so they make sense
    for (rank,) in cursor:
        rank = clean_rank(rank)
        #Add if not already in the list
        if not rank in ranks:
            ranks += (rank,)
    if username == 'jason_kull':
        ranks += ('SysOp',)
    user_data = {'username': username, 'rank': clean_rank(primary_rank), 'ranks': ranks}
    cursor.close()
    with open('Legacy/_users/%s.md' % (slugify(username)), 'w') as outfile:
        data = yaml.safe_dump(user_data, default_flow_style=False)
        outfile.write('---\n%s---\n' % (data))
mcursor.close()
cnx.close()
