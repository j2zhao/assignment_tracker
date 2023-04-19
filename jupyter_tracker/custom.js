define([
    'base/js/namespace',
    'base/js/events'
], function(Jupyter, events) {
    events.on('kernel_ready.Kernel', function() {
        var cell = Jupyter.notebook.get_cell(0);
        var prev_text = cell.get_text();
        if(prev_text.indexOf('%load_ext jupyter_record\n') === -1 ) {
            var cell = IPython.notebook.insert_cell_above('code');
            var notebook_name = Jupyter.notebook.notebook_name;
            cell.set_text('%load_ext jupyter_record\n %set_filename ' + notebook_name);   
        }
        Jupyter.notebook.execute_cells([0]);
    })

});