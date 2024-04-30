from unittest.mock import patch
from base_agent.voice import talk

def test_speaker_initialization_sets_correct_attributes():
    speaker = talk.Speaker(voice='faber-medium', language='pt_BR')
    assert speaker.voice == 'faber-medium'
    assert speaker.language == 'pt_BR'
    assert speaker.model == 'pt_BR-faber-medium'
    assert speaker.outfile == '/tmp/speech.wav'

@patch('voice.talk.sp.Popen')
@patch('voice.talk.sp.call')
def test_speaker_say_calls_correct_commands(mock_call, mock_popen):
    speaker = talk.Speaker()
    mock_popen.return_value.communicate.return_value = (b'', b'')
    speaker.say('Olá como você está?')
    mock_popen.assert_called_once_with(['piper', '--model', 'pt_BR-faber-medium', '--output-file', '/tmp/speech.wav'], stdin=talk.sp.PIPE, stdout=talk.sp.PIPE, stderr=talk.sp.PIPE)
    mock_call.assert_called_once_with(['play', '/tmp/speech.wav'])