document.addEventListener("DOMContentLoaded", function () {
    const rankHeaderFrom = document.getElementById("rank-headging")
    const rankHeaderTo = document.getElementById("rank-heading-goal")
    const rankHeaderPoints = document.getElementById("rank-heading-points")
    const [from, to, difference] = formatRank(300)
    rankHeaderFrom.innerText = from
    rankHeaderTo.innerText = to
    rankHeaderPoints.innerText = `${difference} points`
    
    const flipElements = document.querySelectorAll('td');

    function triggerFlip() {
        flipElements.forEach(element => {
            element.classList.remove('flip');
            setTimeout(() => {
                element.classList.add('flip');
            }, 10);
        });

    }

    setInterval(triggerFlip, 10 * 1000);
})

function formatRank(points) {
    let currentRank = ""
    let nextRank = ""
    let difference = 0

    if (points <= 200) {
        currentRank = "Student"
        nextRank = "Amature"
        difference = 201 - points
    }
    else if (points <= 400) {
        currentRank = "Amature"
        nextRank = "First Officer"
        difference = 401 - points
    }
    else if (points <= 600) {
        currentRank = "First Officer"
        nextRank = "Captain"
        difference = 601 - points
    }
    else if (points <= 800) {
        currentRank = "Captain"
        nextRank = "Instructor"
        difference = 801 - points
    }
    else {
        currentRank = "Instructor"
        nextRank = "Instructor"
    }

    return [currentRank, nextRank, difference]
}