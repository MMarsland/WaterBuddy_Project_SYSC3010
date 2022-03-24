import sys
sys.path.append('../../')
sys.path.append('../../Simulators')
from senseHatDisplay import SenseHatDisplay

def test_init():
    senseDisplay = SenseHatDisplay()
    assert not (senseDisplay == None)

def test_showMessage():
     senseDisplay = SenseHatDisplay()

     senseDisplay.showMessage("Example Message!")
     assert (input('\nDid you see the text "Example Message!"? (y/n): ') == "y")
        
def test_flashWord():
    senseDisplay = SenseHatDisplay()

    delay = 0.2
    senseDisplay.flashWord("Test Flash!", delay)
    
    assert (input(f'\nDid you see the text "Test Flash!" flash with a {delay} second delay? (y/n): ') == "y")

def test_flash():
    senseDisplay = SenseHatDisplay()

    senseDisplay.flash((255,255,0))

    assert (input(f'\nDid you see a yellow flash? (y/n): ') == "y")


def test_getRandomColor():
    senseDisplay = SenseHatDisplay()

    color = senseDisplay.getRandomColour()

    assert color[0] >= 50
    assert color[0] <= 255
    assert isinstance(color[0], int)

    assert color[1] >= 50
    assert color[1] <= 255
    assert isinstance(color[1], int)

    assert color[2] >= 50
    assert color[2] <= 255
    assert isinstance(color[2], int)

