var next_id;

function print_address(response) {
    // get form id
    id = this.id;
    // update values
    $('#attn_'+id).val(response.attn);
    $('#num_'+id).val(response.number);
    $('#dir1_'+id).val(response.dir1);
    $('#street_'+id).val(response.street);
    $('#suffix_'+id).val(response.suffix);
    $('#dir2_'+id).val(response.dir2);
    $('#line2_'+id).val(response.line2);
    // add another form if at end
    if (id == next_id - 1) {
        add_address(next_id);
    }
}

function get_address(serializedData, id){
    return $.ajax({
        url: "split/",
        type: "get",
        dataType: "json",
        id: id,
        data: serializedData
    });
}

function add_ajax_submit(form_name, id) {
    $(form_name).submit(function(event) {
        var $form = $(this),
            $inputs = $form.find("input, select, button, textarea"),
            serializedData = $form.serialize();
        
        get_address(serializedData, id).done(print_address);
        
        event.preventDefault();
    });
}

function add_address(id) {
    // add an address form set
    $('.footer-blocker').before(Mustache.to_html(Mustache.TEMPLATES.address,{
      id: id, 
      slice_id: id % 2
    }));
    
    // add an event listener for this form
    add_ajax_submit("#submit-form_"+id, id);
    
    // increment next_id
    next_id ++
}

$(document).ready(function(){
    next_id = 1;
    
    //add first address lise
    add_address(next_id);

    
});