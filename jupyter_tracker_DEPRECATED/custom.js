define([
    'base/js/namespace',
    'base/js/events'
], function(Jupyter, events) {
    events.on('kernel_ready.Kernel', function() {
        var cell = Jupyter.notebook.get_cell(0);
        var prev_text = cell.get_text();
        if(prev_text.indexOf('%load_ext jupyter_record\n') === -1 ) {
            var cell = IPython.notebook.insert_cell_above('code');
            cell.set_text('%load_ext jupyter_record\n');   
        }
        Jupyter.notebook.execute_cells([0]);
    })

    events.on('create.Cell', function(){
        var cells = Jupyter.notebook.get_cells();
        cells.forEach(function(cell) {
            var prev_text = cell.get_text();
            if(cell.cell_type == 'code' && prev_text.indexOf('%%log_run\n') === -1 && prev_text.indexOf('%load_ext jupyter_record\n') === -1) {
                var text  = '%%log_run\n' + prev_text;
                cell.set_text(text);
            }
        });
    });
});