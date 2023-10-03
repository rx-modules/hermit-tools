# auto-voice-regions
> Dynamically define json files of cuboid regions that control the voice groups that players are in.

## Usage

> **Important**
> [Simple Voice Mod](https://modrinth.com/plugin/simple-voice-chat) and [Enchanced Groups](https://modrinth.com/mod/enhanced-groups) must be installed on the server for this pack

1. Grab the data pack from [here](https://github.com/rx-modules/hermit-tools/releases/tag/avr-v1.0) and load it into your world.
2. Run `/trigger auto_voice_regions` to turn on the data pack
3. Regions defined in the `src/config.json` file will now dynamically control the voice groups of players.

### Triggers

- `/trigger auto_voice_regions` will toggle the data pack on and off
  - This will clean any region displays as well
- `/trigger toggle_region_displays` will toggle the region displays on and off
  - This provides the visuals to the cuboid regions defined for each voice group


### Admin Config

- `/trigger toggle_region_displays` will toggle a visual display of the regions defined in `coords.json`
- `/function auto_voice_regions:main/debug/corner_displays` will add displays for the corners of the regions defined in `coords.json`
  - The red block is the origin and the white one is the corner
  - `/function auto_voice_regions:main/debug/remove_corner_displays` will remove the displays
- `/function auto_voice_regions:main/create_groups` will create persistent voice groups for each region
  - `/function auto_voice_regions:main/remove_groups` will remove them.

## Building

This project uses [`beet`](https://github.com/mcbeet/beet), a python-based build tool to help create data and resource packs. The repo holds uncompiled code that is transformed to vanilla commands. To build the pack:

1. Have a working Python 3.10+ environment (many systems come w/ this pre-installed)
2. Install the requirements via `pip`, a python package manager
  - `pip install -r requirements.lock` or `python -m pip install -r requirements.lock`
3. Clone this repo
  - `git clone https://github.com/rx-modules/hermit-tools`
4. Navigate to this subfolder and run `beet`
  - ```bash
      cd hermit-tools/auto-voice-regions
      beet  # or python -m beet
    ```

## Publishing

This repo auto-builds and attaches the built pack to a release when a version is bumped. To publish a new version:

1. Make changes within `auto-voice-regions`
2. Bump version in `beet.yaml`
3. Commit and push changes
