define([
    'base/js/namespace',
    'base/js/events'
], function(Jupyter, events) {

    function log_cell_execution(data, cell) {
        //var cell = data.cell
        var cell_input = cell.get_text();
        var timestamp = new Date().getTime();
        var notebook_path = Jupyter.notebook.notebook_path;
        var working_directory = notebook_path.split('/').slice(0, -1).join('/');


        var output = data.output;
        // var keys = Object.keys(output).join(", ");
        window.alert(JSON.stringify(data));
        //const keys = Object.getOwnPropertyNames(output).join(", ");
        // var type = output.output_type;
        // console.log('testtest');
        // console.log(output.output_type);
        // if (output.output_type === 'error') {
        //     var errorName = output.ename;
        //     var errorMessage = output.evalue;
        //     var errorTraceback = output.traceback.join('\n');

        //     // Perform any action with the error information, such as logging or storing the data
        //     console.log('Error Name:', errorName);
        //     console.log('Error Message:', errorMessage);
        //     console.log('Error Traceback:', errorTraceback);
        // }
        
        var prev_text = cell.get_text();
        var text  = '%%log_run\n' + prev_text;
        // var text  = output + prev_text;
        cell.set_text(text);

        // cell.element.one("output_appended.OutputArea", function () {
        //     var error_type = "";
        //     var error_message = "";

        //     cell.output_area.outputs.forEach(function (output) {
        //         if (output.output_type === "error") {
        //             error_type = output.ename;
        //             error_message = output.evalue;
        //         }
        //     });

        //     var log_entry = [
        //         "Timestamp: " + timestamp,
        //         "Working Directory: " + working_directory,
        //         "Cell content:\n" + cell_input,
        //         "Error type: " + error_type,
        //         "Error message: " + error_message,
        //         "\n---\n",
        //     ].join("\n");

        //     var prev_text = cell.get_text();
        //     // var text  = log_entry + prev_text;
        //     var text  = '%%log_run\n' + prev_text;
        //     cell.set_text(text);

        //     // write_to_file(cell, log_entry);
        // });
    }
        
    events.on("execute.CodeCell", function (evt, data) {
            log_cell_execution(data, data.cell);
    });
});