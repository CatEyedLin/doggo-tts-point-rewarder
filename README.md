# doggo-tts-point-rewarder
Reads Twitch.tv channel point rewards in windows text-to-speach

In order to use this program fully you will need:
  -the name of you twitch channel
  -an account for the program to use to read chat
  -a OAuth token, i recommend using https://twitchapps.com/tmi/ to get one
  -- if you want it to use a channel point redeem your twitch channel must have access to channel points (be a twitch affiliate or partner)
  
config file details:
  channel - the lowercase username of twitch channel’s chat you want the program to read from
  bot_user_name – the lowercase username or the twitch account that you want this program to use
  bot_login_token – the OAuth token of the twitch account that you want this program to use, i recommend using https://twitchapps.com/tmi/ to get one

  tts_custom_reward_id - the channel reward id of the text reward, that you want to use for TSS, you can find it by redeeming it, and copying the id from the black terminal window
  force_tts_prefix - the single character prefix that when used in the twitch chat will cause the TSS to read the message, as long as the chatter is the broadcaster or allowed by the settings below
  force_tts_allow_mod - allows chat moderators to force a TTS message
  force_tts_allow_all - allows all chatters to force a TTS message

  winX – the number of pixels in the width of window contents 
  winY – the number of pixels in the height of window contents, i recommended setting these to size of your images below
  
  idle_image – the image shown when the TTS is inactive 
  open_image– the image shown when the TTS is active 

  voice_id - the numerical id of the desired TTS voice (read below for more info)
  volume - a number between 0 and 1 such as 0.75 which is the volume of TTS
  words_per_minute – the speed at witch the TTS voice speaks at, in words per minute

Text to speech voices:
  this program pulls voices from “HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens” in the registry, so if you install voices and you can’t get them, look here
  if you download voices though windows settings they will be added to “HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens” simply moving them will work
