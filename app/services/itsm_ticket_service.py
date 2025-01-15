from flask import Flask, request, jsonify
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechRecognizer, SpeechSynthesisResult, ResultReason
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
# from app.model.models import UploadedFile, db
import io
from werkzeug.utils import secure_filename

class TicketOpsService:

    # Azure Speech Service configuration
    SPEECH_SUBSCRIPTION = "your_speech_subscription_key"
    SPEECH_REGION = "your_speech_region"  # e.g., "westus"

    # Azure Blob Storage configuration
    STORAGE_ACCOUNT_NAME = "stgaiititsm01ea"
    STORAGE_ACCOUNT_KEY = "7JAMTy+5j9ZkEHQKWMfdAc6A05+EA1e5b0mAb4Ls7N97kMaVHc9CI+y+qNFXdb7Tkj+m51bh7V7i+AStbGxuUA=="
    VOICE_CONTAINER_NAME = "aiit-itsm-voice"
    USER_PROMPT_CONTAINER_NAME = "aiit-itsm-userprompt"
    SYSTEM_PROMPT_CONTAINER_NAME = "aiit-itsm-systemprompt"
    AICOMPLETION_CONTAINER_NAME = "aiit-itsm-aicompletion"
    BLOB_NAME = "stgaiititsm01ea"

    def transcribe_speech(self, audio_data):
        speech_config = SpeechConfig(subscription=self.SPEECH_SUBSCRIPTION, region=self.SPEECH_REGION)
        audio_config = AudioConfig(stream=audio_data)

        speech_recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        result = speech_recognizer.recognize_once_async().result  # The first result contains the text from the audio

        if result.reason == ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == ResultReason.NoMatch:
            return "No speech could be recognized"
        elif result.reason == ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            return f"Recognition was canceled: {cancellation_details.reason}"

    def upload_to_blob_storage(self, container_name, data):
        container_client = BlobServiceClient.from_connection_string(
            f"DefaultEndpointsProtocol=https;AccountName={self.STORAGE_ACCOUNT_NAME};AccountKey={self.STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
        ).get_container_client(container_name)

        blob_client = container_client.get_blob_client(self.BLOB_NAME)
        blob_client.upload_blob(data, blob_type="BlockBlob")

    def download_from_blob_storage(self, container_name):
        container_client = BlobServiceClient.from_connection_string(
            f"DefaultEndpointsProtocol=https;AccountName={self.STORAGE_ACCOUNT_NAME};AccountKey={self.STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
        ).get_container_client(container_name)

        blob_client = container_client.get_blob_client(self.BLOB_NAME)
        download_stream = io.BytesIO()
        blob_client.download_blob().readinto(download_stream)
        download_stream.seek(0)  # 重置流位置到开始
        return download_stream.read().decode('utf-8')  # 假设Blob内容是UTF-8编码的文本


    # 上传语音文件
    def upload_file(self, file, user_id):
        # Read the file content into a byte array
        file_content = file.read()

        # Convert the byte array to an in-memory stream for the Speech SDK
        audio_stream = io.BytesIO(file_content)
        self.upload_to_blob_storage(self.VOICE_CONTAINER_NAME, audio_stream)
        # Transcribe the speech
        transcribed_text = self.transcribe_speech(audio_stream)

        # Upload the transcribed text to Blob Storage
        self.upload_to_blob_storage(self.USER_PROMPT_CONTAINER_NAME, transcribed_text)

        # uploaded_file = UploadedFile(filename=filename, content=transcribed_text, user_id=user_id)
        # db.session.add(uploaded_file)
        # db.session.commit()
        # return uploaded_file
        return transcribed_text




