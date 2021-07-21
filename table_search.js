// document.getElementById("current_node").innerHTML='ddd


$(document).ready(function(){
  $('#tglr').popover({
    html : true,
    placement: 'bottom', 
    content: function() {
      return $('#popover-content').html();
    } 
});  
});
var column_names = ["URL1","Actual Date Time1","Receiver Email1"];
// var column_names = ["Title","Views","Time","URL","Next boy"];0
var clicks = {title: 0, views: 0, created_on: 0, url: 0};

// draw the table
d3v3.select(".popman").append("div")
.attr("id", "c2")

d3v3.select("#c2").append("div")
.attr("id", "FilterableTable2");

// d3v3.select("#FilterableTable").append("h1")
//   .attr("id", "title")
//   .text("My Youtube Channels")

// d3v3.select("#FilterableTable").append("div")
//   .attr("class", "SearchBar")
//   .append("p")
//     .attr("class", "SearchBar")
//     .text("Search By Title:");

// d3v3.select(".SearchBar")
//   .append("input")
//     .attr("class", "SearchBar")
//     .attr("id", "search")
//     .attr("type", "text")
//     .attr("placeholder", "Search...");

var table = d3v3.select("#FilterableTable2").append("table");
table.append("thead").append("tr"); 

var headers = table.select("tr").selectAll("th")
  .data(column_names)
  .enter()
  .append("th")
  .text(function(d) { return d; });

var rows, row_entries, row_entries_no_anchor, row_entries_with_anchor;
// d3v3.json("data.json", function(data) { // loading data from server

// d3v3.json("wt.json", function(data) { // loading data from server
d3v3.csv("wt.csv", function(error, data) {
console.log(data)
// draw table body with rows
table.append("tbody")

// data bind
rows = table.select("tbody").selectAll("tr")
  .data(data);
console.log(rows)
// enter the rows
rows.enter()
  .append("tr")

// enter td's in each row
row_entries = rows.selectAll("td")
    .data(function(d) { 
      var arr = [];
      for (var k in d) {
        if (d.hasOwnProperty(k)) {
      arr.push(d[k]);
        }
      }
      return [arr[1],arr[2],arr[0]];
    })
  .enter()
    .append("td") 

// draw row entries with no anchor 
row_entries_no_anchor = row_entries.filter(function(d) {
  return (/https?:\/\//.test(d) == false)
})
row_entries_no_anchor.text(function(d) { return d; })

// draw row entries with anchor
row_entries_with_anchor = row_entries.filter(function(d) {
  return (/https?:\/\//.test(d) == true)  
})
row_entries_with_anchor
  .append("a")
  .attr("href", function(d) { return d; })
  .attr("target", "_blank")
  .attr("onclick","window.open(this.href, 'newwindow','width=500,height=450')")
  // .attr("return", "false;")
  // .attr("target", "_blank")
.text(function(d) { return d; })
  
  
/**  search functionality **/
  d3v3.select("#search")
    .on("keyup", function() { // filter according to key pressed 
      var searched_data = data,
          text = this.value.trim();
      var searchResults = searched_data.map(function(r) {
        var regex = new RegExp("^" + text + ".*", "i");
        if (regex.test(r.title)) { // if there are any results
          return regex.exec(r.title)[0]; // return them to searchResults
        } 
      })
    
    // filter blank entries from searchResults
      searchResults = searchResults.filter(function(r){ 
        return r != undefined;
      })
      
      // filter dataset with searchResults
      searched_data = searchResults.map(function(r) {
         return data.filter(function(p) {
          return p.title.indexOf(r) != -1;
        })
      })

      // flatten array 
  searched_data = [].concat.apply([], searched_data)
      
      // data bind with new data
  rows = table.select("tbody").selectAll("tr")
    .data(searched_data)
  
      // enter the rows
      rows.enter()
       .append("tr");
       
      // enter td's in each row
      row_entries = rows.selectAll("td")
          .data(function(d) { 
            var arr = [];
            for (var k in d) {
              if (d.hasOwnProperty(k)) {
            arr.push(d[k]);
              }
            }
            return [arr[3],arr[1],arr[2],arr[0]];
          })
        .enter()
          .append("td") 

      // draw row entries with no anchor 
      row_entries_no_anchor = row_entries.filter(function(d) {
        return (/https?:\/\//.test(d) == false)
      })
      row_entries_no_anchor.text(function(d) { return d; })

      // draw row entries with anchor
      row_entries_with_anchor = row_entries.filter(function(d) {
        return (/https?:\/\//.test(d) == true)  
      })
      row_entries_with_anchor
        .append("a")
        .attr("href", function(d) { return d; })
        .attr("target", "_blank")
      .text(function(d) { return d; })
      
      // exit
      rows.exit().remove();
    })
  
/**  sort functionality **/
headers
  .on("click", function(d) {
    if (d == "Title") {
      clicks.title++;
      // even number of clicks
      if (clicks.title % 2 == 0) {
        // sort ascending: alphabetically
        rows.sort(function(a,b) { 
          if (a.title.toUpperCase() < b.title.toUpperCase()) { 
            return -1; 
          } else if (a.title.toUpperCase() > b.title.toUpperCase()) { 
            return 1; 
          } else {
            return 0;
          }
        });
      // odd number of clicks  
      } else if (clicks.title % 2 != 0) { 
        // sort descending: alphabetically
        rows.sort(function(a,b) { 
          if (a.title.toUpperCase() < b.title.toUpperCase()) { 
            return 1; 
          } else if (a.title.toUpperCase() > b.title.toUpperCase()) { 
            return -1; 
          } else {
            return 0;
          }
        });
      }
    } 
    if (d == "Views") {
    clicks.views++;
      // even number of clicks
      if (clicks.views % 2 == 0) {
        // sort ascending: numerically
        rows.sort(function(a,b) { 
          if (+a.views < +b.views) { 
            return -1; 
          } else if (+a.views > +b.views) { 
            return 1; 
          } else {
            return 0;
          }
        });
      // odd number of clicks  
      } else if (clicks.views % 2 != 0) { 
        // sort descending: numerically
        rows.sort(function(a,b) { 
          if (+a.views < +b.views) { 
            return 1; 
          } else if (+a.views > +b.views) { 
            return -1; 
          } else {
            return 0;
          }
        });
      }
    } 
    if (d == "Created On") {
      clicks.created_on++;
      if (clicks.created_on % 2 == 0) {
        // sort ascending: by date
        rows.sort(function(a,b) { 
          // grep date and time, split them apart, make Date objects for comparing  
        var date = /[\d]{4}-[\d]{2}-[\d]{2}/.exec(a.created_on);
        date = date[0].split("-"); 
        var time = /[\d]{2}:[\d]{2}:[\d]{2}/.exec(a.created_on);
        time = time[0].split(":");
        var a_date_obj = new Date(+date[0],(+date[1]-1),+date[2],+time[0],+time[1],+time[2]);
        
          date = /[\d]{4}-[\d]{2}-[\d]{2}/.exec(b.created_on);
        date = date[0].split("-"); 
        time = /[\d]{2}:[\d]{2}:[\d]{2}/.exec(b.created_on);
        time = time[0].split(":");
        var b_date_obj = new Date(+date[0],(+date[1]-1),+date[2],+time[0],+time[1],+time[2]);
              
          if (a_date_obj < b_date_obj) { 
            return -1; 
          } else if (a_date_obj > b_date_obj) { 
            return 1; 
          } else {
            return 0;
          }
        });
      // odd number of clicks  
      } else if (clicks.created_on % 2 != 0) { 
        // sort descending: by date
        rows.sort(function(a,b) { 
          // grep date and time, split them apart, make Date objects for comparing  
        var date = /[\d]{4}-[\d]{2}-[\d]{2}/.exec(a.created_on);
        date = date[0].split("-"); 
        var time = /[\d]{2}:[\d]{2}:[\d]{2}/.exec(a.created_on);
        time = time[0].split(":");
        var a_date_obj = new Date(+date[0],(+date[1]-1),+date[2],+time[0],+time[1],+time[2]);
        
          date = /[\d]{4}-[\d]{2}-[\d]{2}/.exec(b.created_on);
        date = date[0].split("-"); 
        time = /[\d]{2}:[\d]{2}:[\d]{2}/.exec(b.created_on);
        time = time[0].split(":");
        var b_date_obj = new Date(+date[0],(+date[1]-1),+date[2],+time[0],+time[1],+time[2]);
              
          if (a_date_obj < b_date_obj) { 
            return 1; 
          } else if (a_date_obj > b_date_obj) { 
            return -1; 
          } else {
            return 0;
          }
        });
      }
    }
    if (d == "URL") {
      clicks.url++;
    // even number of clicks
      if (clicks.url % 2 == 0) {
        // sort ascending: alphabetically
        rows.sort(function(a,b) { 
          if (a.thumb_url_default.toUpperCase() < b.thumb_url_default.toUpperCase()) { 
            return -1; 
          } else if (a.thumb_url_default.toUpperCase() > b.thumb_url_default.toUpperCase()) { 
            return 1; 
          } else {
            return 0;
          }
        });
      // odd number of clicks  
      } else if (clicks.url % 2 != 0) { 
        // sort descending: alphabetically
        rows.sort(function(a,b) { 
          if (a.thumb_url_default.toUpperCase() < b.thumb_url_default.toUpperCase()) { 
            return 1; 
          } else if (a.thumb_url_default.toUpperCase() > b.thumb_url_default.toUpperCase()) { 
            return -1; 
          } else {
            return 0;
          }
        });
      }	
    }      
  }) // end of click listeners
});
d3v3.select(self.frameElement).style("height", "780px").style("width", "1150px");	