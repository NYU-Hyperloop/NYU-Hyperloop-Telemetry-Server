var open_leds = [];
var closed_leds = [];
createLeds();
createButtons();


function updateLeds(states) {
    open_leds.forEach(function(led, i) {
        var state = states >>> i;
        led.update(state & 1);
    });
    states = states >>> 6;
    closed_leds.forEach(function(led, i) {
        var state = states >>> i;
        led.update(state & 1);
    });
}


function Led(parent) {
    this.cell = $("<td>");
    this.element = $("<div>");
    this.element.addClass("circle");
    this.cell.append(this.element);

    this.render = function() {
        parent.append(this.cell);
    }

    this.update = function(state) {
        if (state) {
            var color = "green";
        } else {
            var color = "red";
        }
        this.element.css("background-color", color);
    }
}


function createLeds() {
    var parentOpen = $("#open");
    var parentClosed = $("#closed");
    for (var i = 0; i < 6; i++) {
        open_leds.push(new Led(parentOpen));
    }
    for (var i = 0; i < 6; i++) {
        closed_leds.push(new Led(parentClosed));
    }
    open_leds.forEach(function(led) {
        led.render();
    });
    closed_leds.forEach(function(led) {
        led.render();
    });
}


function Button(parent, i) {
    var that = this
    this.i = i
    this.cell = $("<td>");
    this.element = $("<button>")
    this.element.text("*");

    this.element.on("click", function() {
        socket.emit("arduino_command", {
            cmd: "p" + that.i,
        });
    });

    this.cell.append(this.element);
    
    this.render = function() {
        parent.append(this.cell);
    };
}


function createButtons() {
    var buttons = $("#buttons");
    for (var i = 0; i < 6; i++) {
        var button = new Button(buttons, i);
        button.render();
    }
}
