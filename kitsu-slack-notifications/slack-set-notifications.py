
import gazu
from pprint import pprint
import sys

import os
from slack_sdk import WebClient

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SLACK_BOT_TOKEN=os.getenv("SLACK_BOT_TOKEN")
GAZU_API_URL=os.getenv("GAZU_API_URL")
GAZU_LOGIN_EMAIL=os.getenv("GAZU_LOGIN_EMAIL")
GAZU_LOGIN_PASSWORD=os.getenv("GAZU_LOGIN_PASSWORD")




def update_all_user_slack_notifications (slack_active = True):

    try: 

        slk = WebClient(token=SLACK_BOT_TOKEN)

        api_response = slk.api_test()

        if api_response['ok']:
            logger.info('API test successful')

    except Exception as e:
        logger.error("Error connecting to Slack API")
        logger.error(e)
        return
    
    gazu.set_host(GAZU_API_URL)
    gazu.log_in(GAZU_LOGIN_EMAIL, GAZU_LOGIN_PASSWORD)


    # get all persons from kitsu, so we can request the slack user id from the slack api
    
    kitsu_persons = gazu.person.all_persons()
    slack_response = slk.users_list()
    slack_persons = slack_response['members']
    next_cursor = slack_response['response_metadata'].get('next_cursor', None)

    while next_cursor:
        slack_response = slk.users_list(cursor=next_cursor)
        slack_persons.extend(slack_response['members'])
        next_cursor = slack_response['response_metadata'].get('next_cursor', None)



    slack_persons_clean = {}

    # get the slack user id for each email address
    for slack_person in slack_persons:

        is_deleted = slack_person.get("deleted", False)
        if is_deleted:
            continue

        email = slack_person.get("profile", {}).get("email", None)
        if email is None:
            continue
 

        slack_id = slack_person.get("id", None)
        if slack_id is None:
            continue


        slack_persons_clean[email] = slack_id


    



    no_slack_user_list = []
    already_set_list = []
    updated_list = []

    for kitsu_person in kitsu_persons:

        id_match = False
        active_match = False
        

        slack_id_for_match = slack_persons_clean.get(kitsu_person["email"], None)

        if slack_id_for_match is None:
            logger.info(f"Could not find slack user id for email: {kitsu_person['email']}")
            no_slack_user_list.append(kitsu_person['email'])
            continue


        
        
        if kitsu_person.get("notifications_slack_userid", None) == slack_id_for_match:
            # logger.info(f"Slack user ID matches set for {kitsu_person['email']}")
            id_match = True
        else:
            kitsu_person["notifications_slack_userid"] = slack_id_for_match
            # kitsu_person["notifications_slack_enabled"] = slack_active
            # logger.info(f"Updated Slack user ID for {kitsu_person['email']}")


        if kitsu_person.get("notifications_slack_enabled", None) == slack_active:
            # logger.info(f"Slack notifications already set for {kitsu_person['email']}")
            active_match = True
        else:
            kitsu_person["notifications_slack_enabled"] = slack_active
            logger.info(f"Updated Slack notifications status for {kitsu_person['email']}")



        if id_match and active_match:
            logger.info(f"Slack notifications and ID already set for {kitsu_person['email']}")
            already_set_list.append(kitsu_person['email'])
            continue

        updated_person = gazu.person.update_person(kitsu_person)
        updated_list.append(kitsu_person['email'])

        logger.debug(updated_person)
        # logger.info(f"Slack notifications updated for user: {kitsu_person['email']}")

    # print results as formatted summary
    logger.info("\n\n========= Summary:======== \n")
    logger.info(f"\n\nTotal Kitsu users: {len(kitsu_persons)}\n")
    logger.info(f"\n\nMatching Slack users found: {len(slack_persons_clean)}\n")

    logger.info(f"\n\n----No slack user found for: {len(no_slack_user_list)}----\n")
    for email in no_slack_user_list:
        logger.info(f"NO SLACK USER: {email}")
    logger.info(f"\n\n----Slack notifications already set correctly for: {len(already_set_list)}----\n")
    for email in already_set_list:
        logger.info(f"ALREADY SET: {email}")
    logger.info(f"\n\n----Updated Slack notifications for: {len(updated_list)}----\n")
    for email in updated_list:
        logger.info(f"UPDATED: {email}")


if __name__ == "__main__":

    update_all_user_slack_notifications()



