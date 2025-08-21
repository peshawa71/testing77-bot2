from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.tl.types import InputPeerChannel
import tqdm
import time
import imageio_ffmpeg as ffmpeg


# Load .env new adding new sponsor, and path err same shexm nama
load_dotenv()

api_id = int(os.getenv("APITELEGRAM_ID2")) 
api_hash = os.getenv("APITELEGRAM_HASH2")
channel_to_send = -1002979232337

DOWNLOADS_DIR = "downloads100"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
client = TelegramClient("session_name", api_id, api_hash)
client.start()

file_exports = "exported"
if not os.path.exists(file_exports):
    os.mkdir(file_exports)
    print(f"Created: {file_exports}")
else:
    print(f"path {file_exports} exsest bro")

def create_path(path_str):
    """
    Create each directory in the given path one by one if it doesn't exist.
    Example: sponsor/taste/i
    """
    parts = path_str.split(os.sep)  # split by folder separator (/ or \)
    current_path = ""

    for part in parts:
        if not part:  # skip empty parts (e.g., if path starts with /)
            continue
        current_path = os.path.join(current_path, part)
        if not os.path.exists(current_path):
            os.mkdir(current_path)
            print(f"Created: {current_path}")
        else:
            print(f"Exists: {current_path}")


def get_available_filename(base_name, ext=".mp4"):
    i = 1
    filename = f"{base_name}{ext}"
    while os.path.exists(filename):
        filename = f"{base_name}_{i}{ext}"
        i += 1
    return filename


def download_sponsor_videos(chat, limit):

    messages = client.get_messages(chat, limit=limit)

    reverse_data = messages[::-1]


    for msg in tqdm.tqdm(reverse_data):

        # if msg.media and not msg.id == 9 and not msg.id == 4:
        if msg.media:
            # current_path1 = create_path(f"taste/{msg.text}")
        # if msg.media: and "sponsor_onscreen" in msg.text 


            # for message2 in tqdm.tqdm(messages) if message2.media and "چیرۆکی شەوێک" in message2.text and message2.id == max_id:
            #     current_max_id = msg.id
            #     DOWNLOAD_VIDEO = message2

            

            try:

                namefile = get_available_filename(f"sponsors/{msg.message}")
                if "images" in msg.message :
                    namefile = get_available_filename(f"sponsors/{msg.message}", "")


                print(f"\n 📥 Downloading media from message ID {msg.id} {msg.text} loading...")
                filename = client.download_media(msg, namefile)
                print(f"{filename} dowmnloaded")

                if filename:

                    print(f"\n✅ Downloaded: {filename}")
                    

            except Exception as e:
                print(f"❌ file Error : {e}")
# exporting :     # final = concatenate_videoclips(clips, method="compose")
    # final.write_videofile("with_sponsors.mp4", codec="libx264", audio_codec="aac")


def edit_video(video_path):
    client.send_message(-1002979232337,"editing starts!")
    main_video = VideoFileClip(video_path)
    print(f"video durtion = {main_video.duration}")
    client.send_message(-1002979232337,f"{main_video.duration} ")


    if main_video.duration > 25*60:
    # if main_video:
        print("video starts editing... loading")
        cut_place_1 = 6
        cut_place_2 = 22 # cut in minuite 22
        cut_place_3 = main_video.duration - 20 # for setting cut before 1 min to END
        cut_place_4 = main_video.duration
        
        # taste_part:
        # cut_place_1 = 6*60
        # cut_place_2 = 22*60 # cut in minuite 22
        # cut_place_3 = main_video.duration - 2 # for tessting its 2 sec
        # cut_place_4 = main_video.duration
        #video sponsor_onscreen logo_clip = resize(logo_clip, width=1980, height=1080)# set > durtion logo
        # Load the base sponsor image

        # sponsor_beggning = ImageClip("sponsors/images/sponsor_2sec.png").set_duration(2) # setting sponsors & timing 

        split_1 = main_video.subclip(0, cut_place_1)
        shortsponsor1 = VideoFileClip("sponsors/videos/shortsponsor_1.mp4")

        split_2 = main_video.subclip(cut_place_1, cut_place_2)
        allsponsor1 = VideoFileClip("sponsors/videos/allsponsor1.mp4")

        split_3 = main_video.subclip(cut_place_2, cut_place_3)

        split_4 = main_video.subclip(cut_place_3, cut_place_4)
        allsponsor2 = VideoFileClip("sponsors/videos/allsponsor2.mp4")

        final_clip = concatenate_videoclips([split_1, shortsponsor1, split_2, allsponsor1, split_3, allsponsor2, split_4, allsponsor2]) # coneccting them together
        # final_clip = concatenate_videoclips([main_withlogo]) >>> for tasting only
        output_filename = get_available_filename("exported/new_video")

        # final_clip = concatenate_videoclips([split_1, split_2]) >>> taste

        final_clip.write_videofile(
            output_filename,
            codec="libx264",
            preset="ultrafast",
            ffmpeg_params=["-crf", "0"],   # CRF 0 = lossless
            audio_codec="aac"
        )
    
        
        return output_filename


def download_and_forward(chat, limit):
    # isdownload = True
    messages = client.get_messages(chat, limit=limit)

    reverse_data = messages[::-1]

    # all_listed_id = [message.id for message in messages if "چیرۆکی شەوێک" in message.text and message.media]

    # max_id = max(all_listed_id) if all_listed_id else print("No messages found with the specified text and media.")


    for msg in tqdm.tqdm(reverse_data):


        if msg.media and "چیرۆکی شەوێک" in msg.text:
        # if msg.media:

            # for message2 in tqdm.tqdm(messages) if message2.media and "چیرۆکی شەوێک" in message2.text and message2.id == max_id:
            #     current_max_id = msg.id
            #     DOWNLOAD_VIDEO = message2

            try:
                
                print(f"\n📥 Downloading media from message ID {msg.id} {msg.text}...")
                filename = client.download_media(msg, DOWNLOADS_DIR)

                if filename:
                    print(f"\n✅ Downloaded: {filename}")


                    # Send to another channel
            except Exception as e:
                print(f"❌ file Error : {e}")

            
            edited_path = edit_video(filename)
            if edited_path is None:

                print(f"❌ Error: edited path = {edited_path}Edited path is None, skipping file.")
                client.send_message(-1002979232337,f"❌ Error: edited path = {edited_path}Edited path is None, skipping file.")
                continue
            else:
                client.send_message(-1002979232337,f"❌ Error: edited path = {edited_path}sending file.")
                client.send_file(channel_to_send, edited_path, caption=f"{msg.text}", supports_streaming=True)
                print(f"🚀 Sent {edited_path} to {channel_to_send}\n")
                # Delete file
                os.remove(filename)
                os.remove(edited_path)
                print(f"🗑️ Deleted {filename}")



if __name__ == "__main__":

    limit = 300 # its 100 if we have a tekall hh.
    source = "@reng_tv"
    sponsor_source = "sponsor_hadia"

    download_sponsor_videos(sponsor_source, 20)
    download_and_forward(source, limit)
    # download_sponsor_videos(sponsor_source, limit)
