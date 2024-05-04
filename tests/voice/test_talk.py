from unittest.mock import patch
from base_agent.voice import talk

def test_speaker_initialization_sets_correct_attributes():
    speaker = talk.Speaker(language='pt_BR')
    assert speaker.voice == 'faber-medium'
    assert speaker.language == 'pt_BR'
    assert speaker.model == 'pt_BR-faber-medium'
    assert speaker.outfile == '/tmp/speech.wav'

