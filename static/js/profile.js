document.addEventListener("DOMContentLoaded", function () {
    const rankHeader = document.getElementById("rank-headging")
    rankHeader.innerText = formatRank(300)

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
    let rank = ""

    if (points <= 200) rank = "Student"
    else if (points <= 400) rank = "Amature"
    else if (points <= 600) rank = "First Officer"
    else if (points <= 800) rank = "Captain"
    else rank = "Instructor"

    return "Rank - " + rank
}