import streamlit as st


def main():
    st.markdown("## How to use the application?")


    # Display .mov video
    video_file = open("./tutorial.mov", "rb")
    video_bytes = video_file.read()
    st.video(video_bytes, format='video/quicktime')



if __name__ == "__main__":
    main()

# video_file = open('myvideo.mp4', 'rb')
# video_bytes = video_file.read()

# st.video(video_bytes)
# menu()
