const currentDate = new Date();

let tomorrow = new Date();
tomorrow.setDate(currentDate.getDate() + 1);

let nextThreeWeeks = new Date();
nextThreeWeeks.setDate(currentDate.getDate() + 21);

const isMobile = window.innerWidth < 768;

new AirDatepicker("#id_appointment-scheduled_date", {
  position: "top left",
  dateFormat: "yyyy-M-d",
  minDate: tomorrow,
  maxDate: nextThreeWeeks,
  autoClose: true,
  isMobile: isMobile
});

new AirDatepicker("#id_appointment-scheduled_time", {
  position: "top left",
  onlyTimepicker: true,
  timepicker: true,
  minHours: 8,
  maxHours: 20,
  minutesStep: 10
});
