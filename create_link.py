#!python3
# Mark Bykerk KauffmanO.
# Parses command line args and uses VideoLinkCreator to create a link to a URL for a video.
# Sample Use: python create_link.py --learnfqdn "kauffman380011.ddns.net" --key "1237d7ee-80ab-123c-afc5-123ddd7c31bc" --secret "kL1239NnNk0s1234UUm0muL19Xmt1234" --course_id "uuid:fc005cb3865a486981f221bd24111007" --video_url "https:www.microsoft.com" --title "Microsoft Home" --description "A link to Microsoft"
import argparse
import datetime
from panopto_oauth2 import PanoptoOAuth2
from panopto_uploader import PanoptoUploader
from video_link_creator import VideoLinkCreator
import time
import urllib3

def parse_argument():
    '''
    Argument definition and handling.
    '''
    parser = argparse.ArgumentParser(description='Create content at the root of an Ultra course that is a URL.')
    parser.add_argument('--learnfqdn', dest='learnfqdn', required=True, help='Learn Server name as FQDN')
    parser.add_argument('--key', dest='key', required=True, help='Registered REST API Key')
    parser.add_argument('--secret', dest='secret', required=True, help='Registered REST API Secret')
    parser.add_argument('--course_id', dest='course_id', required=True, help='courseId where we create the content. courseId:<id>|uuid:<uuid>|pk1')
    parser.add_argument('--video_url', dest='video_url', required=True, help='The https link to the video.')
    parser.add_argument('--title', dest='title', required=True, help='Title for the content of the link.')
    parser.add_argument('--description', dest='description', required=True, help='Description for the link.')
   
    return parser.parse_args()


def main():
    '''
    Main method
    '''
    args = parse_argument()

    print("current date and time is..")
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime)

    link_creator = VideoLinkCreator(args.learnfqdn, args.key, args.secret, args.course_id, args.video_url, args.title, args.description)
    link_creator.create_video_link()

    print("current date and time is..")
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime)

if __name__ == '__main__':
    main()
