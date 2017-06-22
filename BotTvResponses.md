# Bot TV available responses 
Responses are organized by type of results. One result type is designed to describe a result field format.

| Result Type   | Examples   |
| :--------     | :--------  |
| [volume](#result-type-volume)         | [Monte le son](#monte-le-son-coco)<br>   [Baisse le son](#baisse-le-son)<br>  [Coupe le son](#coupe-le-son)<br> |
| [player](#result-type-player)         | [Mets pause](#mets-pause)<br>[Play](#Play)<br>[Chaine suivante](#chaine-suivante)<br>|
| [device](#result-type-device)         | [Eteinds le décodeur](#eteinds-le-décodeur)<br> [Allume la télé](#allume-la-télé)<br> |
| [station](#result-type-station)       | [Change de chaîne](#zapper-sur-tf1)<br> [Chaîne inexistante](#zapper-sur-tf1xxx)<br> |


# Result type : volume
## Description
The resultType **volume** corresponds to an action on the sound output of the device used by the user.
```json
{
    "resultType": "volume",
    "result": {
        "action": string
    },
    ...
}
```

- `action` : Enumeration string field that can be
    + `up`
    + `down`
    + `mute_on`
    + `mute_off`
    + `mute_toggle`

[Return to top](#bot-tv-available-responses)

## Example
### Monte le son coco
**Response**
```json
{
    "resultType": "volume",
    "result": {
        "action": "up"
    },
}
```

### Baisse le son
**Response**
```json
{
    "resultType": "volume",
    "result": {
        "action": "down"
    },
}
```

### Coupe le son
**Response**
```json
{
    "resultType": "volume",
    "result": {
        "action": "mute_on"
    },
}
```

[Return to top](#bot-tv-available-responses)

# Result type : player
## Description
The resultType **player** corresponds to an action executed on an application which can switch from a media to another. Its structure is as follows :
```json
{
    "resultType": "player",
    "result": {
        "action": string
    },
    ...
}
```

- `action` : Enumeration string field that can be
    + `next`
    + `previous`
    + `pause`
    + `play`
    + `replay`

[Return to top](#bot-tv-available-responses)

## Examples
### Mets pause
**Response**
```json
{
    "resultType": "player",
    "result": {
        "action": "pause"
    },
}
```

### Play
**Response**
```json
{
    "resultType": "player",
    "result": {
        "action": "play"
    },
}
```

### Chaine suivante
**Response**
```json
{
    "resultType": "player",
    "result": {
        "action": "next"
    },
}
```

[Return to top](#bot-tv-available-responses)


# Result type : device
## Description
The resultType **device** corresponds to an action the device currently being used by the user.
```json
{
    "resultType": "device",
    "result": {
        "action": string
    },
    ...
}
```

- `action` : Enumeration string field that can be
    + `SHUT_DOWN`
    + `TURN_ON`

[Return to top](#bot-tv-available-responses)

## Example
### Eteinds le décodeur
**Response**
```json
{
    "resultType": "device",
    "result": {
        "action": "SHUT_DOWN"
    },
}
```

### Allume la télé
**Response**
```json
{
    "resultType": "device",
    "result": {
        "action": "TURN_ON"
    },
}
```

# Result type : station
## Descritpion
The resultType **station** corresponds to an action on the channel number of the device used by the user.
```json
{
    "resultType": "station",
    "result": {
        "station": string,
        "epgId": number,
        "target": string,
        "zappingMode": boolean,
        "lcn": number
        },
    ...
}
```
[Return to top](#bot-tv-available-responses)

## Example
### Zapper sur TF1
**Response**
```json
{
    "resultType": "station",
    "result": {
        "station": "TF1",
        "epgId": 192,
        "target": "mobile",
        "zappingMode": true,
        "lcn": 1
    },
    ...
}
```
### Zapper sur TF1XXX
**Response**
```json
{
    "resultType": "empty",
    "result": null,
    "message": {
        "text": "Désolé, je n'ai pas trouvé la chaine tf1xxx dans la TV d'orange",
        "display": "Désolé, je n'ai pas trouvé la chaine tf1xxx dans la TV d'orange"
    },
    "status": {
        "code": 1609,
        "message": "Unknown station.",
        "description": "Désolé, je n'ai pas trouvé la chaine tf1xxx dans la TV d'orange"
    },
    ...
}
```

[Return to top](#bot-tv-available-responses)
