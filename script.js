async function fetchPrices() {
    try {
        // Cache buster for local fetch
        const response = await fetch('prices.json?t=' + new Date().getTime());
        const data = await response.json();
        
        // Put serviced apartments first
        const apartments = data.filter(d => d.type === 'apartment');
        const hotels = data.filter(d => d.type === 'hotel');
        const sortedData = [...apartments, ...hotels];
        
        window.pricesData = sortedData;
        renderBoard(sortedData);
    } catch (e) {
        console.error("Failed to fetch prices:", e);
    }
}

document.getElementById('riverside-price').addEventListener('change', () => {
    if (window.pricesData) {
        renderBoard(window.pricesData);
    }
});

function renderBoard(data) {
    const board = document.getElementById('board');
    if (board) board.innerHTML = ''; // clear

    const riversidePrice = parseFloat(document.getElementById('riverside-price').value) || 100;

    data.forEach(item => {
        const row = document.createElement('div');
        row.className = 'row';

        // 1. PROPERTY
        const nameDiv = document.createElement('div');
        nameDiv.className = 'col-name type-' + item.type;
        nameDiv.textContent = item.name.toUpperCase();
        row.appendChild(nameDiv);

        // 2. PRICE/NIGHT
        const priceDiv = document.createElement('div');
        priceDiv.className = 'col-price' + (item.is_stale ? ' stale' : '');
        priceDiv.textContent = "$" + item.price;
        row.appendChild(priceDiv);

        // 3. DAILY VARIANCE
        const dailyStr = item.diff === 0 ? "0" : String(Math.abs(item.diff));
        const dailyDiv = document.createElement('div');
        dailyDiv.className = 'col-trend ' + item.trend.toLowerCase();
        dailyDiv.textContent = dailyStr;
        row.appendChild(dailyDiv);

        // 4. WEEKLY VARIANCE
        let diff7d = item.diff_7d || 0;
        let trend7d = "flat";
        let weeklyStr = "STABLE";
        if (diff7d > 0) {
            weeklyStr = "↑ " + diff7d + " USD";
            trend7d = "up";
        } else if (diff7d < 0) {
            weeklyStr = "↓ " + Math.abs(diff7d) + " USD";
            trend7d = "down";
        }
        const weeklyDiv = document.createElement('div');
        weeklyDiv.className = 'col-diff ' + trend7d;
        weeklyDiv.textContent = weeklyStr;
        row.appendChild(weeklyDiv);

        // 5. VS RIVERSIDE (30D)
        let avgDiffPctStr = "N/A";
        let avgPctClass = "flat";
        if (item.avg_30d && item.avg_30d > 0 && riversidePrice > 0) {
            const avgPct = ((item.avg_30d - riversidePrice) / riversidePrice) * 100;
            if (avgPct > 0) {
                avgDiffPctStr = "+" + avgPct.toFixed(1) + "%";
                avgPctClass = "up";
            } else if (avgPct < 0) {
                avgDiffPctStr = avgPct.toFixed(1) + "%";
                avgPctClass = "down";
            } else {
                avgDiffPctStr = "0.0%";
            }
        }
        const avgDiv = document.createElement('div');
        avgDiv.className = 'col-avg-diff ' + avgPctClass;
        avgDiv.textContent = avgDiffPctStr;
        row.appendChild(avgDiv);

        // 6. VS RIVERSIDE %
        let diffPctStr = "N/A";
        let pctClass = "flat";
        if (item.price > 0 && riversidePrice > 0) {
            const pct = ((item.price - riversidePrice) / riversidePrice) * 100;
            if (pct > 0) {
                diffPctStr = "+" + pct.toFixed(1) + "%";
                pctClass = "up";
            } else if (pct < 0) {
                diffPctStr = pct.toFixed(1) + "%";
                pctClass = "down";
            } else {
                diffPctStr = "0.0%";
            }
        }
        const pctDiv = document.createElement('div');
        pctDiv.className = 'col-pct ' + pctClass;
        pctDiv.textContent = diffPctStr;
        row.appendChild(pctDiv);

        if (board) board.appendChild(row);
    });
}

// init
fetchPrices();
