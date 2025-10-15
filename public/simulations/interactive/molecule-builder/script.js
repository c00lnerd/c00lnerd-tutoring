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
const subscriptChallenge = document.getElementById('subscript-challenge');
const formulaBuilder = document.getElementById('formula-builder');
const checkFormulaButton = document.getElementById('check-formula');
const showFormulaHintButton = document.getElementById('show-formula-hint');
const revealFormulaButton = document.getElementById('reveal-formula');
const subscriptFeedback = document.getElementById('subscript-feedback');
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
let lastSubmissionTime = 0; // Track last submission to prevent spam
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
    
    // Add event listener for the new submit button in game area
    const submitGameResultsButton = document.getElementById('submit-game-results');
    if (submitGameResultsButton) {
        submitGameResultsButton.addEventListener('click', showResults);
    }
    
    // Subscript challenge events
    checkFormulaButton.addEventListener('click', checkSubscripts);
    showFormulaHintButton.addEventListener('click', showFormulaHint);
    revealFormulaButton.addEventListener('click', revealCorrectFormula);
    
    // Naming challenge events
    checkNameButton.addEventListener('click', checkCompoundName);
    showHintButton.addEventListener('click', showNamingHint);
    revealAnswerButton.addEventListener('click', revealCompoundName);
    compoundNameInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            checkCompoundName();
        }
    });
    
    // Clear feedback when student starts typing again
    compoundNameInput.addEventListener('input', function() {
        if (namingFeedback.classList.contains('incorrect')) {
            namingFeedback.style.display = 'none';
            compoundNameInput.style.borderColor = '#ddd';
            compoundNameInput.style.backgroundColor = 'white';
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
    resetSubscriptChallenge();
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

    // Calculate the correct formula for checking
    const compound = calculateCompoundFormula(cation, anion);
    
    if (compound) {
        currentCompound = { ...compound, cation, anion };
        displaySubscriptChallenge(cation, anion, compound);
        showFeedback('Now balance the formula by entering the correct subscripts!', 'success');
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

// Display subscript challenge (student must enter subscripts)
function displaySubscriptChallenge(cation, anion, correctCompound) {
    compoundDisplay.classList.add('active');
    subscriptChallenge.style.display = 'block';
    namingChallenge.style.display = 'none';
    compoundFormula.style.display = 'none';
    
    // Build the formula input interface
    formulaBuilder.innerHTML = '';
    
    // Cation part
    const cationPart = document.createElement('div');
    cationPart.className = 'formula-part';
    
    const cationDisplay = document.createElement('span');
    cationDisplay.className = 'ion-display';
    cationDisplay.textContent = cation.element;
    cationPart.appendChild(cationDisplay);
    
    // Only show subscript input if more than 1 is needed
    if (correctCompound.cationCount > 1) {
        const cationSubscript = document.createElement('input');
        cationSubscript.type = 'number';
        cationSubscript.className = 'subscript-input';
        cationSubscript.id = 'cation-subscript';
        cationSubscript.min = '1';
        cationSubscript.max = '9';
        cationSubscript.placeholder = '?';
        cationPart.appendChild(cationSubscript);
    }
    
    formulaBuilder.appendChild(cationPart);
    
    // Anion part
    const anionPart = document.createElement('div');
    anionPart.className = 'formula-part';
    
    const anionDisplay = document.createElement('span');
    anionDisplay.className = 'ion-display';
    
    // Handle polyatomic ions with parentheses
    const needsParentheses = (anion.element.length > 2 || (anion.element.includes('O') && anion.element.length > 1)) && correctCompound.anionCount > 1;
    
    if (needsParentheses) {
        anionDisplay.textContent = '(' + anion.element + ')';
    } else {
        anionDisplay.textContent = anion.element;
    }
    
    anionPart.appendChild(anionDisplay);
    
    // Only show subscript input if more than 1 is needed
    if (correctCompound.anionCount > 1) {
        const anionSubscript = document.createElement('input');
        anionSubscript.type = 'number';
        anionSubscript.className = 'subscript-input';
        anionSubscript.id = 'anion-subscript';
        anionSubscript.min = '1';
        anionSubscript.max = '9';
        anionSubscript.placeholder = '?';
        anionPart.appendChild(anionSubscript);
    }
    
    formulaBuilder.appendChild(anionPart);
    
    resetSubscriptChallenge();
}

// Check student's subscript answers
function checkSubscripts() {
    if (!currentCompound) return;
    
    const cationInput = document.getElementById('cation-subscript');
    const anionInput = document.getElementById('anion-subscript');
    
    let studentCationCount = 1;
    let studentAnionCount = 1;
    
    // Get student's answers (default to 1 if no input field)
    if (cationInput) {
        studentCationCount = parseInt(cationInput.value) || 0;
    }
    if (anionInput) {
        studentAnionCount = parseInt(anionInput.value) || 0;
    }
    
    // Debug logging
    console.log('Student answers:', studentCationCount, studentAnionCount);
    console.log('Correct answers:', currentCompound.cationCount, currentCompound.anionCount);
    
    // Check if correct
    const isCorrect = (studentCationCount === currentCompound.cationCount) && 
                     (studentAnionCount === currentCompound.anionCount);
    
    console.log('Is correct:', isCorrect);
    
    if (isCorrect) {
        subscriptFeedback.textContent = '🎉 Correct! The charges are balanced!';
        subscriptFeedback.className = 'subscript-feedback correct';
        subscriptFeedback.style.display = 'block';
        
        // Show the complete formula and move to naming challenge
        setTimeout(() => {
            showCompletedFormula();
        }, 1500);
        
    } else {
        subscriptFeedback.textContent = '❌ Not quite right. Check your charge balancing!';
        subscriptFeedback.className = 'subscript-feedback incorrect';
        subscriptFeedback.style.display = 'block';
        
        // Add visual emphasis to the input fields
        const cationInput = document.getElementById('cation-subscript');
        const anionInput = document.getElementById('anion-subscript');
        
        if (cationInput) {
            cationInput.style.borderColor = '#dc3545';
            cationInput.style.backgroundColor = '#fff5f5';
        }
        if (anionInput) {
            anionInput.style.borderColor = '#dc3545';
            anionInput.style.backgroundColor = '#fff5f5';
        }
        
        // Reset input styling after 3 seconds
        setTimeout(() => {
            if (cationInput) {
                cationInput.style.borderColor = '#ddd';
                cationInput.style.backgroundColor = '#f8f9fa';
            }
            if (anionInput) {
                anionInput.style.borderColor = '#ddd';
                anionInput.style.backgroundColor = '#f8f9fa';
            }
        }, 3000);
    }
}

// Show formula hint
function showFormulaHint() {
    if (!currentCompound) return;
    
    const cation = currentCompound.cation;
    const anion = currentCompound.anion;
    
    let hint = `💡 Hint: ${cation.name} has a charge of ${cation.charge > 0 ? '+' : ''}${cation.charge}, `;
    hint += `and ${anion.name} has a charge of ${anion.charge}.\n`;
    hint += `To balance the charges, you need the total positive charge to equal the total negative charge.\n`;
    hint += `Think: How many of each ion do you need?`;
    
    subscriptFeedback.textContent = hint;
    subscriptFeedback.className = 'subscript-feedback hint';
}

// Reveal the correct formula
function revealCorrectFormula() {
    if (!currentCompound) return;
    
    const cationInput = document.getElementById('cation-subscript');
    const anionInput = document.getElementById('anion-subscript');
    
    if (cationInput) {
        cationInput.value = currentCompound.cationCount;
    }
    if (anionInput) {
        anionInput.value = currentCompound.anionCount;
    }
    
    subscriptFeedback.textContent = `✅ The correct formula is: ${currentCompound.formula}. ` +
        `You need ${currentCompound.cationCount} ${currentCompound.cation.name} ion(s) and ` +
        `${currentCompound.anionCount} ${currentCompound.anion.name} ion(s) to balance the charges.`;
    subscriptFeedback.className = 'subscript-feedback correct';
    
    setTimeout(() => {
        showCompletedFormula();
    }, 2000);
}

// Show the completed formula and move to naming challenge
function showCompletedFormula() {
    subscriptChallenge.style.display = 'none';
    compoundFormula.style.display = 'block';
    compoundFormula.textContent = currentCompound.formula;
    namingChallenge.style.display = 'block';
    resetNamingChallenge();
}

// Reset subscript challenge interface
function resetSubscriptChallenge() {
    subscriptFeedback.className = 'subscript-feedback';
    subscriptFeedback.style.display = 'none';
}

// Show "Next Compound" button after completing a compound
function showNextCompoundButton() {
    // Create next compound button if it doesn't exist
    let nextButton = document.getElementById('next-compound-btn');
    if (!nextButton) {
        nextButton = document.createElement('button');
        nextButton.id = 'next-compound-btn';
        nextButton.className = 'btn btn-success';
        nextButton.innerHTML = '🚀 Build Next Compound';
        nextButton.style.marginTop = '15px';
        nextButton.style.fontSize = '1.1em';
        nextButton.addEventListener('click', startNextCompound);
        
        // Add it after the compound answer section
        compoundAnswer.appendChild(nextButton);
    }
    nextButton.style.display = 'block';
}

// Start next compound (clear everything and reset)
function startNextCompound() {
    // Hide the next compound button
    const nextButton = document.getElementById('next-compound-btn');
    if (nextButton) {
        nextButton.style.display = 'none';
    }
    
    // Clear everything and reset for next compound
    clearSelection();
    
    // Show encouraging message
    showFeedback('Ready for the next compound! Select your ions and build!', 'success');
}

// Reset naming challenge interface
function resetNamingChallenge() {
    compoundNameInput.value = '';
    compoundNameInput.style.borderColor = '#ddd';
    compoundNameInput.style.backgroundColor = 'white';
    namingFeedback.className = 'naming-feedback';
    namingFeedback.style.display = 'none';
    compoundAnswer.style.display = 'none';
    
    // Hide next compound button
    const nextButton = document.getElementById('next-compound-btn');
    if (nextButton) {
        nextButton.style.display = 'none';
    }
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
            // Add "Next Compound" button after showing the answer
            setTimeout(() => {
                showNextCompoundButton();
            }, 2000);
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
        namingFeedback.textContent = '❌ Incorrect! Try again or use a hint!';
        namingFeedback.className = 'naming-feedback incorrect';
        namingFeedback.style.display = 'block'; // Ensure it's visible
        
        // Add visual emphasis by briefly highlighting the input field
        compoundNameInput.style.borderColor = '#dc3545';
        compoundNameInput.style.backgroundColor = '#fff5f5';
        
        // Reset input styling after 2 seconds
        setTimeout(() => {
            compoundNameInput.style.borderColor = '#ddd';
            compoundNameInput.style.backgroundColor = 'white';
        }, 2000);
        
        // Record incorrect attempt
        sessionData.compounds.push({
            formula: currentCompound.formula,
            name: currentCompound.name,
            wasCorrect: false,
            studentAnswer: studentAnswer,
            timestamp: new Date()
        });
        
        // Clear the feedback after 4 seconds to encourage another try
        setTimeout(() => {
            namingFeedback.style.display = 'none';
        }, 4000);
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

// Validation functions
function isValidName(name) {
    // Check for reasonable name patterns
    if (name.length < 2 || name.length > 50) return false;
    
    // Must contain at least one letter
    if (!/[a-zA-Z]/.test(name)) return false;
    
    // Reject names that are mostly random characters
    const randomPattern = /^[a-zA-Z]{8,}$/; // 8+ consecutive letters (likely random)
    if (randomPattern.test(name.replace(/\s/g, ''))) {
        // Check if it looks like random gibberish (no vowels or too many consonants)
        const vowels = (name.match(/[aeiouAEIOU]/g) || []).length;
        const consonants = (name.match(/[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]/g) || []).length;
        if (vowels === 0 || consonants > vowels * 3) return false;
    }
    
    // Reject names with too many numbers or special characters
    const specialChars = (name.match(/[^a-zA-Z\s\-'\.]/g) || []).length;
    if (specialChars > 2) return false;
    
    return true;
}

function isValidEmail(email) {
    if (!email) return true; // Email is optional
    
    // Basic email format validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) return false;
    
    // Reject obviously fake domains
    const fakeDomains = ['test.com', 'fake.com', 'spam.com', 'temp.com'];
    const domain = email.split('@')[1]?.toLowerCase();
    if (fakeDomains.includes(domain)) return false;
    
    return true;
}

function hasMinimumActivity() {
    // Require at least 2 compounds attempted and 1 minute of activity
    const minDuration = 60000; // 1 minute in milliseconds
    const currentTime = new Date();
    const sessionDuration = currentTime - sessionData.startTime;
    
    return compoundsBuilt >= 2 && sessionDuration >= minDuration;
}

// Start the game
function startGame() {
    const name = studentNameInput.value.trim();
    if (!name) {
        alert('Please enter your name to start the game.');
        return;
    }
    
    // Validate name
    if (!isValidName(name)) {
        alert('Please enter a valid name. Names should be 2-50 characters and contain letters.');
        return;
    }
    
    const email = studentEmailInput.value.trim();
    
    // Validate email if provided
    if (email && !isValidEmail(email)) {
        alert('Please enter a valid email address or leave it blank.');
        return;
    }
    
    studentName = name;
    studentEmail = email;
    
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
    
    // Validate submission before sending
    if (!isValidName(studentName)) {
        emailStatus.textContent = '❌ Invalid student name. Cannot submit results.';
        emailStatus.className = 'email-status error';
        return;
    }
    
    if (studentEmail && !isValidEmail(studentEmail)) {
        emailStatus.textContent = '❌ Invalid email address. Cannot submit results.';
        emailStatus.className = 'email-status error';
        return;
    }
    
    if (!hasMinimumActivity()) {
        emailStatus.textContent = '❌ Insufficient activity. Please complete at least 2 compounds and spend at least 1 minute practicing.';
        emailStatus.className = 'email-status error';
        return;
    }
    
    // Additional spam check - reject if no actual attempts were made
    if (sessionData.totalAttempts === 0) {
        emailStatus.textContent = '❌ No naming attempts recorded. Cannot submit results.';
        emailStatus.className = 'email-status error';
        return;
    }
    
    // Rate limiting - prevent submissions within 30 seconds of each other
    const currentTime = Date.now();
    if (currentTime - lastSubmissionTime < 30000) {
        const waitTime = Math.ceil((30000 - (currentTime - lastSubmissionTime)) / 1000);
        emailStatus.textContent = `❌ Please wait ${waitTime} seconds before submitting again.`;
        emailStatus.className = 'email-status error';
        return;
    }
    
    // Initialize EmailJS
    emailjs.init("ct_s19oZHppLy9BlW");
    
    const duration = Math.round((sessionData.endTime - sessionData.startTime) / 1000 / 60);
    const accuracy = sessionData.totalAttempts > 0 ? 
        Math.round((sessionData.correctAnswers / sessionData.totalAttempts) * 100) : 0;
    
    // Format the message for the existing template with detailed answers
    const compoundsList = sessionData.compounds.map(c => {
        if (c.wasCorrect) {
            return `${c.formula} (${c.name}) - ✅ Correct`;
        } else {
            return `${c.formula} (${c.name}) - ❌ Incorrect
   Student answered: "${c.studentAnswer}"
   Correct answer: "${c.name}"`;
        }
    }).join('\n\n');
    
    const formattedMessage = `Student: ${studentName}
Activity: Molecule Builder Game - Physical Science Module 5

📊 SESSION SUMMARY:
Total Score: ${score} points
Compounds Built: ${compoundsBuilt}
Correct Names: ${sessionData.correctAnswers} / ${sessionData.totalAttempts}
Naming Accuracy: ${accuracy}%
Session Duration: ${duration} minutes

📝 COMPOUNDS PRACTICED:
${compoundsList}

⏰ Submitted: ${new Date().toLocaleString()}`;

    const templateParams = {
        student_name: studentName,
        student_email: studentEmail || 'Not provided',
        message: formattedMessage,
        submission_date: new Date().toLocaleString(),
        from_name: studentName,
        to_name: 'Chuck Summers',
        subject: `Molecule Builder Results - ${studentName}`,
        reply_to: studentEmail || 'noreply@example.com'
    };
    
    emailStatus.textContent = 'Sending results...';
    emailStatus.className = 'email-status';
    
    emailjs.send("service_ot1jg6s", "template_0nxqbk8", templateParams)
        .then(() => {
            lastSubmissionTime = Date.now(); // Record successful submission time
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
    
    // Update progress message
    updateProgressMessage();
}

// Update progress message based on compounds completed
function updateProgressMessage() {
    const progressMessage = document.getElementById('progress-message');
    if (!progressMessage) return;
    
    if (compoundsBuilt < 5) {
        progressMessage.textContent = `🎯 Try to complete at least 10 compounds for best results! (${compoundsBuilt}/10)`;
        progressMessage.parentElement.style.background = '#fff3cd';
        progressMessage.parentElement.style.borderColor = '#ffeaa7';
        progressMessage.style.color = '#856404';
    } else if (compoundsBuilt < 10) {
        progressMessage.textContent = `🚀 Great progress! ${10 - compoundsBuilt} more compounds to reach the recommended 10! (${compoundsBuilt}/10)`;
        progressMessage.parentElement.style.background = '#e3f2fd';
        progressMessage.parentElement.style.borderColor = '#90caf9';
        progressMessage.style.color = '#1565c0';
    } else {
        progressMessage.textContent = `🎉 Excellent! You've completed ${compoundsBuilt} compounds - ready to submit results!`;
        progressMessage.parentElement.style.background = '#e8f5e8';
        progressMessage.parentElement.style.borderColor = '#4CAF50';
        progressMessage.style.color = '#2e7d32';
    }
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
