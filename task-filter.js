function getCompletedTaskTitles(tasks) {
  return tasks
    .filter((task) => task.status === "completed")
    .slice()
    .sort((a, b) => a.id - b.id)
    .map((task) => task.title);
}

module.exports = getCompletedTaskTitles;
