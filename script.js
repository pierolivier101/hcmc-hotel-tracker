const ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$-.+";

const CHAR_FLAP_DELAY = 40; // ms
const MAX_FLAPS = 20;

async function fetchPrices() {
    try {
        // Cache buster for local fetch
        const response = await fetch('prices.json?t=' + new Date().getTime());
        const data = await response.json();
        renderBoard(data);
    } catch (e) {
        console.error("Failed to fetch prices:", e);
    }
}

function renderBoard(data) {
    const board = document.getElementById('board');
    if (board) board.innerHTML = ''; // clear

    data.forEach(item => {
        const row = document.createElement('div');
        row.className = 'row';

        // Formatting
        const namePad = padString(item.name.toUpperCase(), 20);
        const priceStr = "$" + item.price;
        const pricePad = padString(priceStr, 5, true);

        // STATUS column: show actual change figure instead of FLAT/UP/DOWN
        const diffPrefix = item.diff > 0 ? "+" : "";
        const diffStr = item.diff === 0 ? "0" : diffPrefix + item.diff;
        const statusPad = padString(diffStr, 4, true);

        // VARIANCE column: arrow symbol + absolute value
        let arrowStr;
        if (item.diff > 0)       arrowStr = "+" + item.diff + " USD";
        else if (item.diff < 0)  arrowStr = item.diff + " USD";
        else                       arrowStr = "STABLE";
        const variancePad = padString(arrowStr, 10, true);

        // Append components
        createWordDiv(row, namePad, 'col-name type-' + item.type);
        row.querySelector('.col-name').style.flex = "0 0 40%";

        createWordDiv(row, pricePad, 'col-price');
        row.querySelectorAll('.word')[1].style.flex = "0 0 15%";
        row.querySelectorAll('.word')[1].style.justifyContent = "flex-end";

        createWordDiv(row, statusPad, 'col-trend ' + item.trend.toLowerCase());
        row.querySelectorAll('.word')[2].style.flex = "0 0 15%";
        row.querySelectorAll('.word')[2].style.justifyContent = "flex-end";

        createWordDiv(row, variancePad, 'col-diff ' + item.trend.toLowerCase());
        row.querySelectorAll('.word')[3].style.flex = "0 0 30%";
        row.querySelectorAll('.word')[3].style.justifyContent = "flex-end";

        if (board) board.appendChild(row);
    });
}

function padString(str, length, alignRight = false) {
    if (str.length > length) return str.substring(0, length);
    if (alignRight) return str.padStart(length, ' ');
    return str.padEnd(length, ' ');
}

function createWordDiv(rowDiv, text, classNames) {
    const wordDiv = document.createElement('div');
    wordDiv.className = 'word ' + classNames;
    
    for (let i = 0; i < text.length; i++) {
        const flap = document.createElement('div');
        flap.className = 'flap';
        flap.textContent = ' ';
        wordDiv.appendChild(flap);
        
        animateFlap(flap, text[i]);
    }
    
    rowDiv.appendChild(wordDiv);
}

function animateFlap(element, targetChar) {
    let currentIdx = Math.floor(Math.random() * ALPHABET.length);
    let flips = 0;
    const targetFlips = Math.floor(Math.random() * 15) + 10;
    
    const interval = setInterval(() => {
        currentIdx = (currentIdx + 1) % ALPHABET.length;
        element.textContent = ALPHABET[currentIdx];
        flips++;
        
        if (flips >= targetFlips && ALPHABET[currentIdx] === targetChar) {
            clearInterval(interval);
        } else if (flips > targetFlips * 2) {
            // Failsafe
            element.textContent = targetChar;
            clearInterval(interval);
        }
    }, CHAR_FLAP_DELAY);
}

// init
fetchPrices();
