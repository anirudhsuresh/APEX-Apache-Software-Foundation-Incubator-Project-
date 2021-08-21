var flag = 0;
function readTextFile1(file) {
  var rawFile = new XMLHttpRequest();
  rawFile.open("GET", file, false); // using synchronous call
  var allText;
  rawFile.onload = function () {
    if (rawFile.status != 404) {
      // analyze HTTP status of the response
      allText = rawFile.responseText; // e.g. 404: Not Found
      flag = 0;
    } else {
      // show the result
      allText = "No report avaliable for this month";
      flag = 1;
      // add_links(flag)
      // console.log('whysss')
      //alert(`error`); // response is the server response
    }
  };
  //rawFile.onerror = function(){
  //alert(`error`);
  //}
  rawFile.send(null);
  return allText;
}
function update_month_id(the_current_month) {
  document.getElementById("Month").innerHTML = the_current_month;
}
function readTextFile(file) {
  var rawFile = new XMLHttpRequest();
  rawFile.open("GET", file, false); // using synchronous call
  var allText;
  rawFile.onload = function () {
    if (rawFile.status != 404) {
      // analyze HTTP status of the response
      allText = rawFile.responseText; // e.g. 404: Not Found
    } else {
      // show the result
      allText = "No report available for this month";
      //alert(`error`); // response is the server response
    }
  };
  //rawFile.onerror = function(){
  //alert(`error`);
  //}
  rawFile.send(null);
  return allText;
}

// function for getting the project name and convert it to the ids
function myFunction() {
  var this_project = document.getElementById("txt_ide").value;
  var name_to_id = JSON.parse(readTextFile("name_to_id.json"));
  // console.log(this_project)
  var only_name = this_project.split("[")[0].toLowerCase();

  // console.log(only_name)
  var linka = "Mentors_csv/" + only_name.trim() + ".txt";
  var m_paths = `${linka}`;
  // console.log(m_paths)
  var read122 = readTextFile1(m_paths);

  // const list  = document.getElementById('list');

  document.getElementById("mentor").innerHTML = read122;

  // we have stored the name_to_id conversion in order to convert the project name to ids
  var ids = name_to_id[this_project];

  // ----
  // return ids,this_project
  return ids;
}

function getMonth() {
  var this_month = document.getElementById("Month").value;
  console.log(this_month);
  return this_month;
}

function yes() {
  var proj = myFunction();
  var month = getMonth();
  // console.log("---");
  // console.log(proj);

  //var re_m=start_date_dict[month]
  var m = month + ".txt";
  // var link='data1/data1/'+proj+'/'+m
  var link = "data1/" + proj + "/" + m;
  var paths = `${link}`;
  // console.log(paths)
  var read = readTextFile1(paths);
  document.getElementById("textss").value = read;
  add_links();
}

function add_links() {
  if (flag == 0) {
    var month = document.getElementById("Month").value;
    var start_date = JSON.parse(readTextFile("start_date_dict.json"));
    var name_proj = document.getElementById("txt_ide").value;
    var c_month = JSON.parse(readTextFile("month_names_dict.json"));
    var p_idss = name_to_id[name_proj];
    // console.log(p_idss)
    var ac_date = start_date[p_idss];

    // console.log(`${ac_date}`);

    if (month > 12) {
      // console.log('hello1')
      var re_years = parseInt(month / 12);
      var re_months = parseInt(month % 12);
      // console.log(re_months,re_years)
    } else {
      // console.log('hello2')
      var re_years = 0;
      var re_months = month;
      // console.log(re_months,re_years)
    }

    var res = ac_date.split("/");
    // console.log(res)
    // will add all the dates and make the actaul year and month
    var f_year = +re_years + +res[2];
    var f_month = +re_months + +res[0];
    // console.log(f_month)

    if (f_month > 12) {
      // console.log('hello1')
      var fi_year = parseInt(f_month / 12);
      var fi_month = parseInt(f_month % 12);
      // console.log(re_months,re_years)
    } else {
      // console.log('hello2')
      var fi_year = 0;
      var fi_month = f_month;
      // console.log(re_months,re_years)
    }

    var month_inti = fi_month;
    var month_words = c_month[month_inti];
    var ac_proj = name_proj;
    var project_name = ac_proj.split("[");
    var finals_year = +fi_year + +f_year;
    // console.log(finals_year)
    // console.log(month_words)

    // var res = ac_date.split("/");
    // var month_inti=res[0]
    // var month_words=c_month[month_inti]
    var ac_proj = name_proj;
    var project_name = ac_proj.split("[");
    if (finals_year == 2005) {
      // console.log("hello1");
      var final_link =
        "https://cwiki.apache.org/confluence/display/INCUBATOR/IncubatorBoardReport2005Q4";
    } else if (finals_year == 2006) {
      if (month_words == "January") {
        var final_link =
          "https://cwiki.apache.org/confluence/display/INCUBATOR/IncubatorBoardReport2006Q1";
      } else if (month_words == "February") {
        var final_link =
          "https://cwiki.apache.org/confluence/display/INCUBATOR/IncubatorBoardReport2006Q1";
      } else {
        var final_link =
          "https://cwiki.apache.org/confluence/display/INCUBATOR/" +
          month_words +
          finals_year +
          "#" +
          project_name[0];
      }
    } else {
      // console.log('hello3')
      var final_link =
        "https://cwiki.apache.org/confluence/display/INCUBATOR/" +
        month_words +
        finals_year +
        "#" +
        project_name[0];
    }

    // document.getElementById("textss").value = final_link;
    // console.log('<a href="'+final_link+'"> Link </a>')
    document.getElementById("repo_link").innerHTML =
      '<a href="' + final_link + '" target="_blank"> Link </a>';
  } else {
    document.getElementById("repo_link").innerHTML = "No link for this month";
  }
}
