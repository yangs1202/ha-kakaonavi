# ha-kakaonavi

`ha-kakaonavi` is a Home Assistant custom component that integrates with Kakao Mobility's Navigation API to provide real-time estimated travel times and routes between specified locations.

## Installation

1. **Download the Component:**
   - Clone this repository or download the zip file and extract it.
   - Copy the `ha-kakaonavi` directory to your `custom_components` directory in your Home Assistant configuration directory.

2. **Add to Configuration:**
   - Add the following to your `configuration.yaml` file:
     ```yaml
     sensor:
       - platform: ha-kakaonavi
         apikey: YOUR_KAKAO_API_KEY
         start: "Start Address"
         end: "End Address"
         waypoint: "Waypoint Address"  # Optional
     ```

3. **Restart Home Assistant:**
   - Restart Home Assistant to load the new component.

## Configuration

| Parameter | Required | Description |
|-----------|----------|-------------|
| `apikey`  | Yes      | Your Kakao API key. You can obtain it from the Kakao Developers site. |
| `start`   | Yes      | The start address for the navigation. |
| `end`     | Yes      | The end address for the navigation. |
| `waypoint`| No       | An optional waypoint address. |

## Example Configuration

Here's an example configuration:

```yaml
sensor:
  - platform: ha-kakaonavi
    apikey: "your_kakao_api_key"
    start: "1600 Amphitheatre Parkway, Mountain View, CA"
    end: "1 Infinite Loop, Cupertino, CA"
    waypoint: "350 5th Ave, New York, NY"  # Optional
```
