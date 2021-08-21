function updateAll() {
  var this_project = document.getElementById("txt_ide").value;
  forceProperties.selected_data.project = name_to_id[this_project];

  UpdateTechnicalNet();
  UpdateEmailNet();
  UpdateprojectInfo();
}
