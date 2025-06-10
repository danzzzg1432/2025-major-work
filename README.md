# Idle Tutor Tycoon

This repository contains the code for *Idle Tutor Tycoon*, a Python/PyGame based idle/tycoon style game built as part of my 2025 Major Work for the HSC Software Engineering course.

If you decide to download and run the game, please consider providing [feedback](https://docs.google.com/forms/d/1S49IZXE-VYq69Yd1FltCkhzX_Bd-nV-thi6cPYWUfZU/edit)

## Prerequisites

- **Python 3.8+** – the game has been tested with Python 3.11, 3.12 and 3.13.
- **Pip** – Python package manager used to install dependencies.

Download Python here:
- [`Python`](https://www.python.org/downloads/) – handling graphics, input and sound.

Install pip by running these commands inside your command line or terminal:

Windows:
```bash
py -m ensurepip --upgrade
```
macOS:
```bash
python -m ensurepip --upgrade
```
## Installing Dependencies

The game relies on a few third‑party libraries:

- [`pygame-ce`](https://pypi.org/project/pygame-ce/) – handling graphics, input and sound.
- [`ntplib`](https://pypi.org/project/ntplib/) – synchronising timestamps for save files.

Install them using pip:

```bash
pip install pygame-ce ntplib
```

## Project Structure

```
assets/          Game art, fonts and sounds
savestates/      Save file storage (`save_data.json`)
main.py          Entry point for the game
*.py             Game logic, UI and helper modules
```

The `assets` folder must remain in the same directory as `main.py` so that images, fonts and sounds can be loaded correctly. The game automatically writes progress to `savestates/save_data.json` on exit. However, these should clone automatically into a stable format.

## Running the Game

1. Clone or download this repository.
2. Ensure the dependencies above are installed.
3. From the repository root, run:

```bash
python main.py
```
If that doesn't work depending on your system, you may need to append a number at the end of python; e.g.
```bash
python3 main.py
```

The game window should open and you can start playing. Progress will be saved when you exit.

## Troubleshooting

- **Missing modules** – If Python reports a module cannot be found (`ModuleNotFoundError`), double‑check the dependencies were installed in the environment you are using.

## License
This project was developed for educational purposes. Refer to the repository for asset sources and further information.

## Credits
All music credits go to [NoCopyrightSounds](https://ncs.io) and their respective artists.

Button click sound credit goes to Rhodesmas; you may find them [here](https://freesound.org/people/rhodesmas/sounds/380291/)

A massive thank you to the [AdCap Wiki](https://adventure-capitalist.fandom.com/wiki/AdVenture_Capitalist_Wiki) as well. 

Flaticon icons:
t-rex
pocike
Freepik
textstudio.com

