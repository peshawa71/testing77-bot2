from moviepy import editor
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip
import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.tl.types import InputPeerChannel
import tqdm
import time



# Load .env new
load_dotenv()

api_id = int(os.getenv("APITELEGRAM_ID")) 
api_hash = os.getenv("APITELEGRAM_HASH")
channel_to_send = -1002332921402

DOWNLOADS_DIR = "downloads100"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
client = TelegramClient("new_session", api_id, api_hash)
client.start()


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
                if msg.id == 2 and msg.id == 3 and msg.id == 4:
                    namefile = get_available_filename(f"sponsors/{msg.message}", "")


                print(f"\n📥 Downloading media from message ID {msg.id} {msg.text} loading...")
                filename = client.download_media(msg, namefile)
                print(f"{filename} dowmnloaded")

                if filename:

                    print(f"\n✅ Downloaded: {filename}")
                    

            except Exception as e:
                print(f"❌ file Error : {e}")
# exporting :     # final = concatenate_videoclips(clips, method="compose")
    # final.write_videofile("with_sponsors.mp4", codec="libx264", audio_codec="aac")


def edit_video(video_path):

    main_video = VideoFileClip(video_path)

    if main_video.duration > 25*60:

        cut_place_1 = 6*60
        cut_place_2 = 22*60 # cut in minuite 22
        cut_place_3 = main_video.duration - 20 # for setting cut before 1 min to END
        cut_place_4 = main_video.duration
        
        # taste_part:
        # cut_place_1 = 6*60
        # cut_place_2 = 22*60 # cut in minuite 22
        # cut_place_3 = main_video.duration - 2 # for tessting its 2 sec
        # cut_place_4 = main_video.duration


        # def simple_motion(t):
        # return 180, 180
        logo_clip = ImageClip("sponsors/images/logo_gull2bigger.png").set_duration(main_video.duration)
        #video sponsor_onscreen logo_clip = resize(logo_clip, width=1980, height=1080)# set > durtion logo
        logo_clip = logo_clip.set_position((635, 0))
        # Load the base sponsor image
        base_sponsor = ImageClip("sponsors\images\onscreen1.png") \
            .set_duration(17) \
            .set_pos(("center", "bottom")) \
            .fadein(0.5).fadeout(0.5)
        # change this line bro >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        base_sponsor_2 = ImageClip("sponsors\images\onscreen4.png") \
            .set_duration(17) \
            .set_pos(("center", "bottom")) \
            .fadein(0.5).fadeout(0.5)



        # Generate sponsor times every 7 minutes

        sponsor_interval = 7*60 # 7 minutes in seconds ! its both: 17s> sponsor and lets>7min but becarefull in small secounds durtion.
        sponsor_clips = []
        i = 0
        for start_time in range(0, int(main_video.duration), sponsor_interval):
                
            if start_time + 19 < main_video.duration:
                if i % 2 == 0:
                    sponsor2 = base_sponsor_2.copy().set_start(start_time)
                    sponsor_clips.append(sponsor2)
                    i += 1
                else:
                    sponsor = base_sponsor.copy().set_start(start_time)
                    sponsor_clips.append(sponsor)
                    i += 1


        main_withlogo = CompositeVideoClip([main_video, logo_clip]+ sponsor_clips) # add logo



        sponsor_beggning = ImageClip("sponsors\images\sponsor_2sec.png").set_duration(2) # setting sponsors & timing 

        split_1 = main_withlogo.subclip(0, cut_place_1)
        sponsorvideo_1_short = VideoFileClip("sponsors\videos\short_sponsor_1.mp4")

        split_2 = main_withlogo.subclip(cut_place_1, cut_place_2)
        sponsorvideo_2_middle = VideoFileClip("sponsors\videos\allsponsor2.mp4")

        split_3 = main_withlogo.subclip(cut_place_2, cut_place_3)

        editable_video = VideoFileClip("sponsors\videos\allsponsorlongend.mp4").subclip(0, 67)
        hadia1 = VideoFileClip("sponsors\videos\hadia.mp4")
        ghazzah1 = VideoFileClip("sponsors\videos\ghazzah1.mp4")
        sponsorvideo_3_end = CompositeVideoClip([ghazzah1, hadia1, editable_video])
        split_4 = main_withlogo.subclip(cut_place_3, cut_place_4)





        final_clip = concatenate_videoclips([sponsor_beggning, split_1, sponsorvideo_1_short, split_2, sponsorvideo_2_middle, split_3, sponsorvideo_3_end, split_4, sponsorvideo_3_end]) # coneccting them together
        # final_clip = concatenate_videoclips([main_withlogo]) >>> for tasting only
        output_filename = get_available_filename("exported_taste/new_video")
        # final_clip = concatenate_videoclips([split_1, split_2]) >>> taste
        final_clip.write_videofile(output_filename, fps=main_video.fps)

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
                    edited_path = edit_video(filename)


                    # Send to another channel
                    client.send_file(channel_to_send, edited_path, caption=f"{msg.text}", supports_streaming=True)
                    print(f"🚀 Sent to {channel_to_send}\n")

                    # Delete file
                    os.remove(filename)
                    print(f"🗑️ Deleted {filename}")

            except Exception as e:
                print(f"❌ file Error : {e}")


if __name__ == "__main__":

    limit = 300 # its 100 if we have a tekall hh.
    source = "@reng_tv"
    sponsor_source = "@gullsponsors"

    download_sponsor_videos("@gullsponsor", 20)
    download_and_forward(source, limit)
    # download_sponsor_videos(sponsor_source, limit)


