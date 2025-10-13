// Ion data with charges, names, and formulas
const CATIONS = [
    { symbol: 'Na⁺', name: 'Sodium', charge: 1, element: 'Na' },
    { symbol: 'K⁺', name: 'Potassium', charge: 1, element: 'K' },
    { symbol: 'Li⁺', name: 'Lithium', charge: 1, element: 'Li' },
    { symbol: 'Ag⁺', name: 'Silver', charge: 1, element: 'Ag' },
    { symbol: 'H⁺', name: 'Hydrogen', charge: 1, element: 'H' },
    { symbol: 'NH₄⁺', name: 'Ammonium', charge: 1, element: 'NH4' },
    
    { symbol: 'Ca²⁺', name: 'Calcium', charge: 2, element: 'Ca' },
    { symbol: 'Mg²⁺', name: 'Magnesium', charge: 2, element: 'Mg' },
    { symbol: 'Ba²⁺', name: 'Barium', charge: 2, element: 'Ba' },
    { symbol: 'Sr²⁺', name: 'Strontium', charge: 2, element: 'Sr' },
    { symbol: 'Zn²⁺', name: 'Zinc', charge: 2, element: 'Zn' },
    { symbol: 'Cd²⁺', name: 'Cadmium', charge: 2, element: 'Cd' },
    { symbol: 'Pb²⁺', name: 'Lead(II)', charge: 2, element: 'Pb' },
    { symbol: 'Cu²⁺', name: 'Copper(II)', charge: 2, element: 'Cu' },
    { symbol: 'Fe²⁺', name: 'Iron(II)', charge: 2, element: 'Fe' },
    { symbol: 'Mn²⁺', name: 'Manganese(II)', charge: 2, element: 'Mn' },
    { symbol: 'Co²⁺', name: 'Cobalt(II)', charge: 2, element: 'Co' },
    { symbol: 'Ni²⁺', name: 'Nickel(II)', charge: 2, element: 'Ni' },
    
    { symbol: 'Al³⁺', name: 'Aluminum', charge: 3, element: 'Al' },
    { symbol: 'Fe³⁺', name: 'Iron(III)', charge: 3, element: 'Fe' },
    { symbol: 'Cr³⁺', name: 'Chromium(III)', charge: 3, element: 'Cr' }
];

const ANIONS = [
    { symbol: 'Cl⁻', name: 'Chloride', charge: -1, element: 'Cl' },
    { symbol: 'Br⁻', name: 'Bromide', charge: -1, element: 'Br' },
    { symbol: 'I⁻', name: 'Iodide', charge: -1, element: 'I' },
    { symbol: 'F⁻', name: 'Fluoride', charge: -1, element: 'F' },
    { symbol: 'OH⁻', name: 'Hydroxide', charge: -1, element: 'OH' },
    { symbol: 'NO₃⁻', name: 'Nitrate', charge: -1, element: 'NO3' },
    { symbol: 'NO₂⁻', name: 'Nitrite', charge: -1, element: 'NO2' },
    { symbol: 'ClO₃⁻', name: 'Chlorate', charge: -1, element: 'ClO3' },
    { symbol: 'ClO₄⁻', name: 'Perchlorate', charge: -1, element: 'ClO4' },
    { symbol: 'CH₃COO⁻', name: 'Acetate', charge: -1, element: 'CH3COO' },
    { symbol: 'CN⁻', name: 'Cyanide', charge: -1, element: 'CN' },
    { symbol: 'MnO₄⁻', name: 'Permanganate', charge: -1, element: 'MnO4' },
    
    { symbol: 'SO₄²⁻', name: 'Sulfate', charge: -2, element: 'SO4' },
    { symbol: 'SO₃²⁻', name: 'Sulfite', charge: -2, element: 'SO3' },
    { symbol: 'CO₃²⁻', name: 'Carbonate', charge: -2, element: 'CO3' },
    { symbol: 'O²⁻', name: 'Oxide', charge: -2, element: 'O' },
    { symbol: 'S²⁻', name: 'Sulfide', charge: -2, element: 'S' },
    { symbol: 'CrO₄²⁻', name: 'Chromate', charge: -2, element: 'CrO4' },
    { symbol: 'Cr₂O₇²⁻', name: 'Dichromate', charge: -2, element: 'Cr2O7' },
    { symbol: 'HPO₄²⁻', name: 'Hydrogen Phosphate', charge: -2, element: 'HPO4' },
    
    { symbol: 'PO₄³⁻', name: 'Phosphate', charge: -3, element: 'PO4' },
    { symbol: 'N³⁻', name: 'Nitride', charge: -3, element: 'N' }
];

// Game state
let selectedIons = [];
let score = 0;
let compoundsBuilt = 0;

// DOM elements
const studentInfoSection = document.getElementById('student-info-section');
const gameHeader = document.getElementById('game-header');
const studentNameInput = document.getElementById('student-name');
const studentEmailInput = document.getElementById('student-email');
const saveResultsCheckbox = document.getElementById('save-results');
const startGameButton = document.getElementById('start-game');
const studentDisplayName = document.getElementById('student-display-name');
const resultsSection = document.getElementById('results-section');
const sessionSummary = document.getElementById('session-summary');
const submitResultsButton = document.getElementById('submit-results');
const continuePlayingButton = document.getElementById('continue-playing');
const restartGameButton = document.getElementById('restart-game');
const showResultsButton = document.getElementById('show-results');
const emailStatus = document.getElementById('email-status');

const cationGrid = document.getElementById('cation-grid');
const anionGrid = document.getElementById('anion-grid');
const buildingArea = document.getElementById('building-area');
const selectedIonsContainer = document.getElementById('selected-ions');
const buildButton = document.getElementById('build-compound');
const clearButton = document.getElementById('clear-all');
const compoundDisplay = document.getElementById('compound-display');
const compoundFormula = document.getElementById('compound-formula');
const namingChallenge = document.getElementById('naming-challenge');
const compoundNameInput = document.getElementById('compound-name-input');
const checkNameButton = document.getElementById('check-name');
const showHintButton = document.getElementById('show-hint');
const revealAnswerButton = document.getElementById('reveal-answer');
const namingFeedback = document.getElementById('naming-feedback');
const compoundAnswer = document.getElementById('compound-answer');
const correctName = document.getElementById('correct-name');
const compoundInfo = document.getElementById('compound-info');
const scoreElement = document.getElementById('score');
const compoundsBuiltElement = document.getElementById('compounds-built');
const correctNamesElement = document.getElementById('correct-names');
const feedback = document.getElementById('feedback');

// Game state
let currentCompound = null;
let studentName = '';
let studentEmail = '';
let gameStartTime = null;
let sessionData = {
    compounds: [],
    correctAnswers: 0,
    totalAttempts: 0,
    startTime: null,
    endTime: null
};

// Initialize the game
function initGame() {
    createIonElements();
    setupEventListeners();
    updateDisplay();
}

// Create ion elements in the grids
function createIonElements() {
    // Create cations
    CATIONS.forEach(cation => {
        const ionElement = createIonElement(cation, 'cation');
        cationGrid.appendChild(ionElement);
    });

    // Create anions
    ANIONS.forEach(anion => {
        const ionElement = createIonElement(anion, 'anion');
        anionGrid.appendChild(ionElement);
    });
}

// Create individual ion element
function createIonElement(ion, type) {
    const ionDiv = document.createElement('div');
    ionDiv.className = `ion ${type}`;
    ionDiv.draggable = true;
    ionDiv.dataset.ion = JSON.stringify(ion);
    
    ionDiv.innerHTML = `
        <div class="ion-symbol">${ion.symbol}</div>
        <div class="ion-name">${ion.name}</div>
    `;

    // Add drag event listeners
    ionDiv.addEventListener('dragstart', handleDragStart);
    ionDiv.addEventListener('dragend', handleDragEnd);
    ionDiv.addEventListener('click', handleIonClick);

    return ionDiv;
}

// Handle drag start
function handleDragStart(e) {
    e.target.classList.add('dragging');
    e.dataTransfer.setData('text/plain', e.target.dataset.ion);
}

// Handle drag end
function handleDragEnd(e) {
    e.target.classList.remove('dragging');
}

// Handle ion click (alternative to drag and drop)
function handleIonClick(e) {
    const ionData = JSON.parse(e.target.dataset.ion);
    addIonToSelection(ionData);
}

// Setup event listeners
function setupEventListeners() {
    // Drop zone events
    buildingArea.addEventListener('dragover', handleDragOver);
    buildingArea.addEventListener('drop', handleDrop);
    buildingArea.addEventListener('dragleave', handleDragLeave);

    // Button events
    buildButton.addEventListener('click', buildCompound);
    clearButton.addEventListener('click', clearSelection);
    
    // Student info events
    startGameButton.addEventListener('click', startGame);
    
    // Results events
    submitResultsButton.addEventListener('click', submitResults);
    continuePlayingButton.addEventListener('click', continueGame);
    restartGameButton.addEventListener('click', restartGame);
    showResultsButton.addEventListener('click', showResults);
    
    // Naming challenge events
    checkNameButton.addEventListener('click', checkCompoundName);
    showHintButton.addEventListener('click', showNamingHint);
    revealAnswerButton.addEventListener('click', revealCompoundName);
    compoundNameInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            checkCompoundName();
        }
    });
}

// Handle drag over building area
function handleDragOver(e) {
    e.preventDefault();
    buildingArea.classList.add('drag-over');
}

// Handle drag leave building area
function handleDragLeave(e) {
    if (!buildingArea.contains(e.relatedTarget)) {
        buildingArea.classList.remove('drag-over');
    }
}

// Handle drop in building area
function handleDrop(e) {
    e.preventDefault();
    buildingArea.classList.remove('drag-over');
    
    const ionData = JSON.parse(e.dataTransfer.getData('text/plain'));
    addIonToSelection(ionData);
}

// Add ion to selection
function addIonToSelection(ionData) {
    // Check if we already have 4 ions (reasonable limit)
    if (selectedIons.length >= 4) {
        showFeedback('Maximum 4 ions allowed at once!', 'error');
        return;
    }

    selectedIons.push(ionData);
    updateSelectedIonsDisplay();
    showFeedback(`Added ${ionData.name} (${ionData.symbol})`, 'success');
}

// Update selected ions display
function updateSelectedIonsDisplay() {
    selectedIonsContainer.innerHTML = '';
    
    selectedIons.forEach((ion, index) => {
        const ionElement = document.createElement('div');
        ionElement.className = 'selected-ion';
        ionElement.innerHTML = `
            <div class="ion-symbol">${ion.symbol}</div>
            <div class="ion-name">${ion.name}</div>
            <button class="remove-ion" onclick="removeIon(${index})">×</button>
        `;
        selectedIonsContainer.appendChild(ionElement);
    });
}

// Remove ion from selection
function removeIon(index) {
    selectedIons.splice(index, 1);
    updateSelectedIonsDisplay();
}

// Clear all selected ions
function clearSelection() {
    selectedIons = [];
    updateSelectedIonsDisplay();
    compoundDisplay.classList.remove('active');
    resetNamingChallenge();
    showFeedback('Selection cleared!', 'success');
}

// Build compound from selected ions
function buildCompound() {
    if (selectedIons.length === 0) {
        showFeedback('Please select some ions first!', 'error');
        return;
    }

    // Separate cations and anions
    const cations = selectedIons.filter(ion => ion.charge > 0);
    const anions = selectedIons.filter(ion => ion.charge < 0);

    if (cations.length === 0) {
        showFeedback('You need at least one cation (positive ion)!', 'error');
        return;
    }

    if (anions.length === 0) {
        showFeedback('You need at least one anion (negative ion)!', 'error');
        return;
    }

    if (cations.length > 1) {
        showFeedback('Please use only one type of cation at a time!', 'error');
        return;
    }

    if (anions.length > 1) {
        showFeedback('Please use only one type of anion at a time!', 'error');
        return;
    }

    const cation = cations[0];
    const anion = anions[0];

    // Calculate the formula
    const compound = calculateCompoundFormula(cation, anion);
    
    if (compound) {
        currentCompound = { ...compound, cation, anion };
        displayCompoundChallenge(compound);
        showFeedback('Compound built! Now try to name it!', 'success');
    }
}

// Calculate compound formula using charge balancing
function calculateCompoundFormula(cation, anion) {
    const cationCharge = Math.abs(cation.charge);
    const anionCharge = Math.abs(anion.charge);
    
    // Find least common multiple for charge balancing
    const lcm = (cationCharge * anionCharge) / gcd(cationCharge, anionCharge);
    
    const cationCount = lcm / cationCharge;
    const anionCount = lcm / anionCharge;

    // Build formula
    let formula = '';
    
    // Add cation part
    if (cationCount === 1) {
        formula += cation.element;
    } else {
        formula += cation.element + subscript(cationCount);
    }

    // Add anion part
    if (anionCount === 1) {
        formula += anion.element;
    } else {
        // Handle polyatomic ions
        if (anion.element.length > 2 || (anion.element.includes('O') && anion.element.length > 1)) {
            formula += '(' + anion.element + ')' + subscript(anionCount);
        } else {
            formula += anion.element + subscript(anionCount);
        }
    }

    // Generate compound name
    const name = generateCompoundName(cation, anion);
    
    // Determine difficulty based on charges and complexity
    let difficulty = 1;
    if (Math.max(cationCharge, anionCharge) > 1) difficulty = 2;
    if (Math.max(cationCharge, anionCharge) > 2) difficulty = 3;
    if (anion.element.length > 2) difficulty += 1; // Polyatomic ions

    return {
        formula: formula,
        name: name,
        cationCount: cationCount,
        anionCount: anionCount,
        difficulty: difficulty
    };
}

// Generate compound name
function generateCompoundName(cation, anion) {
    let name = cation.name + ' ' + anion.name;
    
    // Handle special cases for transition metals with multiple oxidation states
    if (cation.name.includes('(')) {
        // Already has oxidation state in name
        return name;
    }
    
    return name;
}

// Convert number to subscript
function subscript(num) {
    const subscripts = ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉'];
    return num.toString().split('').map(digit => subscripts[parseInt(digit)]).join('');
}

// Greatest common divisor
function gcd(a, b) {
    return b === 0 ? a : gcd(b, a % b);
}

// Display compound challenge (formula only, student must name it)
function displayCompoundChallenge(compound) {
    compoundFormula.textContent = compound.formula;
    compoundDisplay.classList.add('active');
    resetNamingChallenge();
}

// Reset naming challenge interface
function resetNamingChallenge() {
    compoundNameInput.value = '';
    namingFeedback.className = 'naming-feedback';
    namingFeedback.style.display = 'none';
    compoundAnswer.style.display = 'none';
}

// Check if the student's answer is correct
function checkCompoundName() {
    if (!currentCompound) return;
    
    const studentAnswer = compoundNameInput.value.trim().toLowerCase();
    const correctAnswer = currentCompound.name.toLowerCase();
    
    // Check for exact match or common variations
    const isCorrect = studentAnswer === correctAnswer || 
                     checkAlternativeNames(studentAnswer, correctAnswer);
    
    // Track the attempt
    sessionData.totalAttempts++;
    
    if (isCorrect) {
        namingFeedback.textContent = '🎉 Correct! Well done!';
        namingFeedback.className = 'naming-feedback correct';
        
        // Track correct answer
        sessionData.correctAnswers++;
        
        // Award points and update stats
        updateScore(currentCompound.difficulty);
        compoundsBuilt++;
        
        // Record compound data
        sessionData.compounds.push({
            formula: currentCompound.formula,
            name: currentCompound.name,
            wasCorrect: true,
            studentAnswer: studentAnswer,
            timestamp: new Date()
        });
        
        updateDisplay();
        
        // Show the full answer after a delay
        setTimeout(() => {
            revealCompoundName();
        }, 1500);
        
        // Show results after 10 compounds or suggest submission
        if (compoundsBuilt > 0 && compoundsBuilt % 10 === 0) {
            setTimeout(() => {
                if (confirm(`Great job! You've built ${compoundsBuilt} compounds. Would you like to submit your results now?`)) {
                    showResults();
                }
            }, 3000);
        }
    } else {
        namingFeedback.textContent = '❌ Not quite right. Try again or use a hint!';
        namingFeedback.className = 'naming-feedback incorrect';
        
        // Record incorrect attempt
        sessionData.compounds.push({
            formula: currentCompound.formula,
            name: currentCompound.name,
            wasCorrect: false,
            studentAnswer: studentAnswer,
            timestamp: new Date()
        });
    }
}

// Show a hint for naming the compound
function showNamingHint() {
    if (!currentCompound) return;
    
    const cation = currentCompound.cation;
    const anion = currentCompound.anion;
    
    let hint = `💡 Hint: This compound contains ${cation.name}`;
    if (cation.name.includes('(')) {
        hint += ` (notice the Roman numeral for charge)`;
    }
    hint += ` and ${anion.name}.`;
    
    // Add prefix/suffix hints
    if (anion.name.endsWith('ide')) {
        hint += ` Remember: simple anions end in "-ide".`;
    } else if (anion.name.endsWith('ate')) {
        hint += ` Remember: this polyatomic ion ends in "-ate".`;
    } else if (anion.name.endsWith('ite')) {
        hint += ` Remember: this polyatomic ion ends in "-ite".`;
    }
    
    namingFeedback.textContent = hint;
    namingFeedback.className = 'naming-feedback hint';
}

// Reveal the correct answer
function revealCompoundName() {
    if (!currentCompound) return;
    
    const cation = currentCompound.cation;
    const anion = currentCompound.anion;
    
    correctName.textContent = currentCompound.name;
    
    let info = `This compound is formed by combining `;
    if (currentCompound.cationCount === 1) {
        info += `one ${cation.name} ion`;
    } else {
        info += `${currentCompound.cationCount} ${cation.name} ions`;
    }
    info += ` with `;
    if (currentCompound.anionCount === 1) {
        info += `one ${anion.name} ion`;
    } else {
        info += `${currentCompound.anionCount} ${anion.name} ions`;
    }
    info += `. The charges balance out to form a neutral compound.`;
    
    compoundInfo.textContent = info;
    compoundAnswer.style.display = 'block';
}

// Check for alternative acceptable names
function checkAlternativeNames(student, correct) {
    // Remove extra spaces and handle common variations
    const studentClean = student.replace(/\s+/g, ' ').trim();
    const correctClean = correct.replace(/\s+/g, ' ').trim();
    
    // Handle Roman numeral spacing variations: "chromium (iii)" vs "chromium(iii)"
    const studentNormalized = studentClean.replace(/\s*\(\s*(i+v*|v*i+)\s*\)\s*/gi, '($1)');
    const correctNormalized = correctClean.replace(/\s*\(\s*(i+v*|v*i+)\s*\)\s*/gi, '($1)');
    
    // Check if they match after normalization
    if (studentNormalized === correctNormalized) return true;
    
    // Also check without parentheses entirely
    const studentNoParens = studentClean.replace(/[()]/g, '').replace(/\s+/g, ' ');
    const correctNoParens = correctClean.replace(/[()]/g, '').replace(/\s+/g, ' ');
    
    return studentNoParens === correctNoParens;
}

// Update score
function updateScore(difficulty) {
    score += difficulty * 10;
}

// Start the game
function startGame() {
    const name = studentNameInput.value.trim();
    if (!name) {
        alert('Please enter your name to start the game.');
        return;
    }
    
    studentName = name;
    studentEmail = studentEmailInput.value.trim();
    
    // Initialize session data
    sessionData = {
        compounds: [],
        correctAnswers: 0,
        totalAttempts: 0,
        startTime: new Date(),
        endTime: null
    };
    
    // Show game interface
    studentInfoSection.style.display = 'none';
    gameHeader.style.display = 'block';
    document.querySelector('.game-area').style.display = 'block';
    
    studentDisplayName.textContent = `Student: ${studentName}`;
}

// Continue playing after viewing results
function continueGame() {
    resultsSection.style.display = 'none';
}

// Restart the entire game
function restartGame() {
    // Reset all game state
    score = 0;
    compoundsBuilt = 0;
    selectedIons = [];
    currentCompound = null;
    
    // Reset session data
    sessionData = {
        compounds: [],
        correctAnswers: 0,
        totalAttempts: 0,
        startTime: new Date(),
        endTime: null
    };
    
    // Reset UI
    resultsSection.style.display = 'none';
    gameHeader.style.display = 'none';
    document.querySelector('.game-area').style.display = 'none';
    studentInfoSection.style.display = 'block';
    
    // Clear inputs
    studentNameInput.value = '';
    studentEmailInput.value = '';
    
    updateDisplay();
    clearSelection();
}

// Show results summary
function showResults() {
    sessionData.endTime = new Date();
    const duration = Math.round((sessionData.endTime - sessionData.startTime) / 1000 / 60); // minutes
    
    const accuracy = sessionData.totalAttempts > 0 ? 
        Math.round((sessionData.correctAnswers / sessionData.totalAttempts) * 100) : 0;
    
    sessionSummary.innerHTML = `
        <div class="summary-item">
            <span><strong>Student:</strong></span>
            <span>${studentName}</span>
        </div>
        <div class="summary-item">
            <span><strong>Total Score:</strong></span>
            <span>${score} points</span>
        </div>
        <div class="summary-item">
            <span><strong>Compounds Built:</strong></span>
            <span>${compoundsBuilt}</span>
        </div>
        <div class="summary-item">
            <span><strong>Correct Names:</strong></span>
            <span>${sessionData.correctAnswers} / ${sessionData.totalAttempts}</span>
        </div>
        <div class="summary-item">
            <span><strong>Naming Accuracy:</strong></span>
            <span>${accuracy}%</span>
        </div>
        <div class="summary-item">
            <span><strong>Session Duration:</strong></span>
            <span>${duration} minutes</span>
        </div>
        <div class="summary-item">
            <span><strong>Compounds Practiced:</strong></span>
            <span>${sessionData.compounds.map(c => c.formula).join(', ')}</span>
        </div>
    `;
    
    resultsSection.style.display = 'block';
}

// Submit results via email
function submitResults() {
    if (!saveResultsCheckbox.checked) {
        emailStatus.textContent = 'Results submission is disabled.';
        emailStatus.className = 'email-status error';
        return;
    }
    
    // Initialize EmailJS
    emailjs.init("ct_s19oZHppLy9BlW");
    
    const duration = Math.round((sessionData.endTime - sessionData.startTime) / 1000 / 60);
    const accuracy = sessionData.totalAttempts > 0 ? 
        Math.round((sessionData.correctAnswers / sessionData.totalAttempts) * 100) : 0;
    
    const templateParams = {
        student_name: studentName,
        student_email: studentEmail || 'Not provided',
        activity_name: 'Molecule Builder Game - Physical Science Module 5',
        total_score: score,
        compounds_built: compoundsBuilt,
        correct_answers: sessionData.correctAnswers,
        total_attempts: sessionData.totalAttempts,
        accuracy_percentage: accuracy,
        session_duration: duration,
        compounds_practiced: sessionData.compounds.map(c => 
            `${c.formula} (${c.name}) - ${c.wasCorrect ? 'Correct' : 'Incorrect'}`
        ).join('\n'),
        timestamp: new Date().toLocaleString(),
        reply_to: studentEmail || 'noreply@example.com'
    };
    
    emailStatus.textContent = 'Sending results...';
    emailStatus.className = 'email-status';
    
    emailjs.send("service_ot1jg6s", "template_0nxqbk8", templateParams)
        .then(() => {
            emailStatus.textContent = "✅ Results sent to instructor successfully!";
            emailStatus.className = "email-status success";
        })
        .catch((error) => {
            console.error('Email send failed:', error);
            emailStatus.textContent = "❌ Failed to send results. Please try again.";
            emailStatus.className = "email-status error";
        });
}

// Update display elements
function updateDisplay() {
    scoreElement.textContent = score;
    compoundsBuiltElement.textContent = compoundsBuilt;
    correctNamesElement.textContent = sessionData.correctAnswers;
}

// Show feedback message
function showFeedback(message, type) {
    feedback.textContent = message;
    feedback.className = `feedback ${type}`;
    
    setTimeout(() => {
        feedback.classList.remove('success', 'error');
        feedback.style.display = 'none';
    }, 3000);
}

// Initialize the game when page loads
document.addEventListener('DOMContentLoaded', initGame);
