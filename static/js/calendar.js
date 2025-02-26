document.addEventListener("DOMContentLoaded", function () {
    var calendarEl = document.getElementById("calendar");
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: "dayGridMonth",
      events: "/get_all_user_tasks",
      headerToolbar: {
        left: "prev,next",
        center: "title",
        right: "today,dayGridWeek,dayGridMonth", // user can switch between the two
      },
      views: {
        dayGridMonth: {
          fixedWeekCount: false,
        },
      },
      dayCellClassNames: function(arg) {
        if (arg.isPast) return ["past-day"]
      }
    });
    calendar.render();
  });
  