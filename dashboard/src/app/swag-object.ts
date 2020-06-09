export class SwagObject {
    objectId: string;
    label: string;
    precision: number;
    image_path: string;
    direction: string;
    first_appear: number;
    last_appear: number;
    avg_speed: number;
    max_speed: number;

    constructor(data: String) {
        this.objectId = data["objectId"];

        var label_with_precision = this.getMax(data['labels']);
        this.label = label_with_precision["key"];
        this.precision = label_with_precision["value"].toFixed(2);

        var direction_with_precision = this.getMax(data["move_direction"]);
        this.direction = direction_with_precision["key"];

        this.first_appear = data["first_appear"].toFixed(2);
        this.last_appear = data["last_appear"].toFixed(2);
        this.avg_speed = data["avg_speed"].toFixed(2);
        this.max_speed = data["max_speed"].toFixed(2);
    }

    getMax(arr) {
        var max;
        var value;
        Object.keys(arr).forEach(function(key) {
            if(max == null || value == null || (arr[key] != null && parseFloat(arr[key]) > value)){
                max = key;
                value = arr[key];
            }
        });
        if(value == null){
            value = 0.0;
        }
        if(max == null){
            max = "Unknown";
        }
        return {
            "key": max,
            "value": value
        }
    }
}