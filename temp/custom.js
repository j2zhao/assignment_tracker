define([
    "base/js/namespace",
    "base/js/events",
    "jquery",
    "base/js/utils",
], function (Jupyter, events, $, utils) {
    function write_to_file(cell, new_log_entry, file_index = 0, max_file_size = 1024 * 1024) { // 1 MB by default
        alert("Hello, World!");
        var base_url = Jupyter.notebook.base_url;

        function update_file(file_index, current_content) {
            var updated_content = current_content + new_log_entry;

            // Check if the updated content exceeds the maximum file size
            if (new Blob([updated_content]).size > max_file_size) {
                // Increment the file index and call write_to_file with the updated file name
                file_name = "cell_log_" + (++file_index) + ".txt";
                write_to_file(cell, new_log_entry, file_index, max_file_size);
            } else {
                // Update the file with the new content
                $.ajax({
                    type: "PUT",
                    url: utils.url_path_join(base_url, "api/contents/", file_index),
                    contentType: "application/json",
                    data: JSON.stringify({
                        type: "file",
                        format: "text",
                        content: updated_content,
                    }),
                    success: function () {
                        console.log("Cell log updated successfully");
                    },
                    error: function () {
                        console.error("Error updating the cell log");
                    },
                });
            }
        }

        // Fetch the current content of the file
        file_name = "cell_log_" + (file_index) + ".txt";
        $.ajax({
            type: "GET",
            url: utils.url_path_join(base_url, "api/contents/", file_name),
            contentType: "application/json",
            success: function (data) {
                update_file(file_index, data.content);
            },
            error: function (jqXHR) {
                if (jqXHR.status === 404) {
                    // If the file doesn't exist, create it with an empty content
                    update_file(file_name, "");
                } else {
                    console.error("Error fetching the current content of the cell log");
                }
            },
        });
    }

    function log_cell_execution(cell) {
        var prev_text = cell.get_text();
        var text  = '%%log_run\n' + prev_text;
        cell.set_text(text);
        // var cell_input = cell.get_text();
        // var timestamp = new Date().getTime();
        // var notebook_path = Jupyter.notebook.notebook_path;
        // var working_directory = notebook_path.split('/').slice(0, -1).join('/');

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

        //     write_to_file(cell, log_entry);
        // });
    }

    function load_ipython_extension() {
        var cells = Jupyter.notebook.get_cells();
        
        events.on("execute.CodeCell", function (evt, data) {
            log_cell_execution(data.cell);
        });
    }

    return {
        load_ipython_extension: load_ipython_extension,
    };
});