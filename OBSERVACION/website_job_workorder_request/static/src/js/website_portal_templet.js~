odoo.define('job_workorder_website_request.website_portal_templet', function(require) {

$(document).ready(function(){
    console.log('abcd')
    
    $(".myInput").change(function myFunction() {
          console.log('abcdZZ')
          var input, filter, table, tr, td, i;
          input = document.getElementById("myInput");
          filter = input.value.toUpperCase();
          table = document.getElementById("joborder_table");
          tr = table.getElementsByTagName("tr");
          for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[0];
            if (td) {
              if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
              } else {
                tr[i].style.display = "none";
              }
            }       
          }
        });

    });

}); 
