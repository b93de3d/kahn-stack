const SECOND = 1000;
const MINUTE = 60 * SECOND;
const HOUR = 60 * MINUTE;

export const formatTime = (value: number, workDayHours = 24) => {
  const minusSign = value < 0 ? "-" : "";
  value = Math.abs(value);
  if (value < 1000) {
    return "0s";
  }

  const workDayDuration = workDayHours * HOUR;

  const workDays = Math.floor(value / workDayDuration);
  value -= workDays * workDayDuration;
  const workDaysText = workDays !== 0 ? `${workDays}d` : "";

  const hours = Math.floor(value / HOUR);
  value -= hours * HOUR;
  const hoursText = hours !== 0 ? `${hours}h` : "";

  const minutes = Math.floor(value / MINUTE);
  value -= minutes * MINUTE;
  const minutesText = minutes !== 0 ? `${minutes}m` : "";

  const seconds = Math.floor(value / SECOND);
  const secondsText = hours === 0 && seconds !== 0 ? `${seconds}s` : "";

  return [minusSign, workDaysText, hoursText, minutesText, secondsText]
    .filter((x) => x !== "")
    .join(" ");
};
