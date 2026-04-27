const ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$-.+↑↓";

const CHAR_FLAP_DELAY = 40; // ms
const MAX_FLAPS = 20;

async function fetchPrices() {
    try {
        // Cache buster for local fetch
        const response = await fetch('prices.json?t=' + new Date().getTime());
        const data = await response.json();
        
        // Put serviced apartments first
        const apartments = data.filter(d => d.type === 'apartment');
        const hotels = data.filter(d => d.type === 'hotel');
        const sortedData = [...apartments, ...hotels];
        
        renderBoard(sortedData);
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

        // DAILY VARIANCE column: show absolute value (valeur absolue)
        const dailyStr = item.diff === 0 ? "0" : String(Math.abs(item.diff));
        const statusPad = padString(dailyStr, 5, true);

        // WEEKLY VARIANCE column: arrow symbol + 7-day average absolute value
        let weeklyStr;
        let diff7d = item.diff_7d || 0;
        
        let trend7d = "flat";
        if (diff7d > 0) {
            weeklyStr = "↑ " + diff7d + " USD";
            trend7d = "up";
        } else if (diff7d < 0) {
            weeklyStr = "↓ " + Math.abs(diff7d) + " USD";
            trend7d = "down";
        } else {
            weeklyStr = "STABLE";
        }
        const variancePad = padString(weeklyStr, 11, true);

        // Append components
        createWordDiv(row, namePad, 'col-name type-' + item.type);
        createWordDiv(row, pricePad, 'col-price');
        createWordDiv(row, statusPad, 'col-trend ' + item.trend.toLowerCase());
        createWordDiv(row, variancePad, 'col-diff ' + trend7d);

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
