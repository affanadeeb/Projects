// chatGPT
function getTimeDifference(timestamp){
    const now = Date.now();
    const diff = now - timestamp;
  
    // Calculate time differences in milliseconds, seconds, minutes, hours, days, and weeks
    const msInSecond = 1000;
    const msInMinute = 60 * msInSecond;
    const msInHour = 60 * msInMinute;
    const msInDay = 24 * msInHour;
    const msInWeek = 7 * msInDay;
  
    // Calculate time differences
    const secondsAgo = Math.floor(diff / msInSecond);
    const minutesAgo = Math.floor(diff / msInMinute);
    const hoursAgo = Math.floor(diff / msInHour);
    const daysAgo = Math.floor(diff / msInDay);
    const weeksAgo = Math.floor(diff / msInWeek);
  
    if (secondsAgo < 60) {
      return `${secondsAgo} ${secondsAgo === 1 ? 'second' : 'seconds'} ago`;
    } else if (minutesAgo < 60) {
      return `${minutesAgo} ${minutesAgo === 1 ? 'minute' : 'minutes'} ago`;
    } else if (hoursAgo < 24) {
      return `${hoursAgo} ${hoursAgo === 1 ? 'hour' : 'hours'} ago`;
    } else if (daysAgo < 7) {
      return `${daysAgo} ${daysAgo === 1 ? 'day' : 'days'} ago`;
    } else {
      // Format the date
      const date = new Date(timestamp);
      const formattedDate = date.toDateString();
      return formattedDate;
    }
  };
  
  
const getDate = (timestamp) => {
    const dateObject = new Date(timestamp);
  
    const year = dateObject.getFullYear();
    const month = dateObject.getMonth() + 1;
    const day = dateObject.getDate();
  
    return {
      day: day,
      month: month,
      year: year,
    };
};
  
const getTimestamp = () => {
    return new Date().getTime();
}

export {getTimeDifference, getDate, getTimestamp};