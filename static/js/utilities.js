function format_word(string) {
    if (string.indexOf("-") != -1) {
        string = "(" + string.replace(/-/g, ":") + ")";
    }
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function format_text(text) {
    var name = ''
    var parts = text.split('_');
    for (var i in parts) {
        name += ' ';
        name += format_word(parts[i]);
    }
    return name.slice(1);
}

function update_option_names(data) {
    var pod_runs = data['pod_runs'];
    var selector = document.getElementById('graph_picker');
    selector.options.length = 0;

    var group = document.getElementById('graph_picker_none');
    var option = document.createElement("option");
    option.value = "blank";
    option.text = "No graph selected";
    group.appendChild(option);

    var group = document.getElementById('graph_picker_runs');
    for (var s in data['pod_runs']) {
        var option = document.createElement("option");
        option.value = data['pod_runs'][s];
        option.text = format_text(data['pod_runs'][s]);
        group.appendChild(option);
    }

    var group = document.getElementById('graph_picker_sensors');
    for (var s in data['sensors']) {
        var option = document.createElement("option");
        option.value = data['sensors'][s];
        option.text = format_text(data['sensors'][s]);
        group.appendChild(option);
    }
}

function deleteGraph() {
    var selector = document.getElementById('graph_picker');
    var name = selector.options[selector.selectedIndex].value;
    if (name.indexOf("run_") != -1) {
        selector.remove(selector.selectedIndex);
        socket.emit('server_command', {
            cmd: 'delete_run',
            name: name
        });
    }
}