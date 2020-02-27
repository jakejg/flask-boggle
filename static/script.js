const form = document.querySelector('form')
const word = document.querySelector('#guess')
const messageDiv = document.querySelector('#message')
const scoreDiv = document.querySelector('#score')
const timerDiv = document.querySelector('#timer')
const highScoreDiv = document.querySelector('#highscore')
let score = 0
let time = 20

form.addEventListener('submit', sendFormData)

function updateHighScore(highscore) {
    highScoreDiv.innerText = `High Score: ${highscore}`
}

async function endGame(){
    form.classList.add('hide')
    response = await axios.post('/post-score', {score: score})
    console.log(response.data['score'])
    updateHighScore(response.data['score'])
}

function countDown(){
    let timerID = setInterval(function() {
        time --
        timerDiv.innerText = `Time left ${time} seconds`
        if (time === 0) {
            clearInterval(timerID)
            endGame() 
        }
    } , 1000)
    
}

async function sendFormData(evt) {
    evt.preventDefault()
    

    const response = await axios.get("/check", { params: { word: word.value }})
    const message = response.data['result']
  
    showMessage(message)
    
    if (message == "Okay!") {
        updateScore()
    }
    form.reset()
}

function showMessage(message){
    messageDiv.innerText = ""
    if (message === "Okay!") {
        messageDiv.style.backgroundColor = "green"
    }
    else {
        messageDiv.style.backgroundColor = "red"
    }
    messageDiv.innerText = message

}

function updateScore(){
    score += word.value.length
    scoreDiv.innerText = `Score: ${score}`
    
}

countDown()