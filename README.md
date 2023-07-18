# Chrome Extension Update Watcher
This is a Python script which provides update notifications for Chrome extensions. It is also able to automatically deobfuscate the extension's source and generate diffs between two versions. The script then exports these results to a Discord webhook.

## Usage:
1. Clone this repository.
2. Install [webcrack](https://github.com/j4k0xb/webcrack) by running `npm install -g webcrack`. Make sure it is in your PATH.
3. Install this project's dependencies by running `pip3 install -r requirements.txt`.
4. Run `python3 main.py` to generate the config file.
5. Edit `config/config.json`. The configuration options are detailed in the next section.
6. Run `python3 main.py` to download the extensions you configured. Running this file in the future will also check for updates and report them to the configured webhook.
7. (optional) Put `main.py` on a cron job to run it repeatedly. 

## Configuration:
- `watched_extensions` - A dict of extensions that the script will check for updates, with the extension ID as the key and any options as the value.
- `discord_webhooks` - A list of strings containing Discord webhook URLs to report to.
- `collapse_diffs` - If this is set to true, the generated diffs will be in one file, instead of being split up for each modified file.
- `debug` - If this is set to true, the logging level will be set to `logging.DEBUG` instead of `logging.INFO`.

### Extension Options:
Extension options should be specified as a dict. All settings in this list are optional.
 - `update_url` - The custom update server for the extension. This defaults to Google's official servers.
 - `name_override` - Overrides the extension's name.

### Example Config File:
```json
{
  "watched_extensions": {
    "haldlgldplgnggkjaafhelgiaglafanh": {
      "update_url": "https://ext.goguardian.com/stable.xml"
    },
    "joflmkccibkooplaeoinecjbmdebglab": {
      "update_url": "https://extensions.securly.com/extensions.xml"
    },
    "pgmjaihnmedpcdkjcgigocogcbffgkbn": {},
    "iheobagjkfklnlikgihanlhcddjoihkg": {
      "name_override": "Securly for Chromebooks (old)"
    },
    "ddfbkhpmcdbciejenfcolaaiebnjcbfc": {}
  },
  "discord_webhooks": [
    "https://discord.com/api/webhooks/xxxxxxxxxxxxxx/xxxxxxxxxxxxxx"
  ],
  "collapse_diffs": true,
  "debug": false
}
```

## Copyright Notice:

This project uses [webcrack](https://github.com/j4k0xb/webcrack) for the deobfuscation of JS files. 
```
ading2210/ext-watcher: A Python program for Chrome extension update notifications.
Copyright (C) 2023 ading2210

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```