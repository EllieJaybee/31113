import aiohttp
import crescent
import hikari
from pydub import AudioSegment
import speech_recognition

plugin = crescent.Plugin()
recognizer = speech_recognition.Recognizer()

@plugin.include
@crescent.message_command(name="Process voice")
async def voice(ctx: crescent.Context, message: hikari.Message):
	if not hikari.MessageFlag.IS_VOICE_MESSAGE in message.flags:
		return await ctx.respond(content="not voice", ephemeral=True)
	await ctx.defer(ephemeral=True)
	with open("f.mp3", mode="wb") as f:
		async with aiohttp.ClientSession() as session:
			async with session.get(message.attachments[0].url) as response:
				thing = await response.read()
				f.write(thing)
	
	sound = AudioSegment.from_mp3("f.mp3")
	sound.export("f.wav", format="wav")

	with speech_recognition.AudioFile("f.wav") as source:
		audio_data = recognizer.record(source)
		text = recognizer.recognize_google(audio_data)
	
	await ctx.respond(text, ephemeral=True)