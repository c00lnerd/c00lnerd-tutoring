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
const cationGrid = document.getElementById('cation-grid');
const anionGrid = document.getElementById('anion-grid');
const buildingArea = document.getElementById('building-area');
const selectedIonsContainer = document.getElementById('selected-ions');
const buildButton = document.getElementById('build-compound');
const clearButton = document.getElementById('clear-all');
const compoundDisplay = document.getElementById('compound-display');
const compoundFormula = document.getElementById('compound-formula');
const compoundName = document.getElementById('compound-name');
const compoundInfo = document.getElementById('compound-info');
const scoreElement = document.getElementById('score');
const compoundsBuiltElement = document.getElementById('compounds-built');
const feedback = document.getElementById('feedback');

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
        displayCompound(compound, cation, anion);
        updateScore(compound.difficulty);
        compoundsBuilt++;
        updateDisplay();
        showFeedback(`Great! You built ${compound.name}!`, 'success');
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

// Display the built compound
function displayCompound(compound, cation, anion) {
    compoundFormula.textContent = compound.formula;
    compoundName.textContent = compound.name;
    
    let info = `This compound is formed by combining `;
    if (compound.cationCount === 1) {
        info += `one ${cation.name} ion`;
    } else {
        info += `${compound.cationCount} ${cation.name} ions`;
    }
    info += ` with `;
    if (compound.anionCount === 1) {
        info += `one ${anion.name} ion`;
    } else {
        info += `${compound.anionCount} ${anion.name} ions`;
    }
    info += `. The charges balance out to form a neutral compound.`;
    
    compoundInfo.textContent = info;
    compoundDisplay.classList.add('active');
}

// Update score
function updateScore(difficulty) {
    score += difficulty * 10;
}

// Update display elements
function updateDisplay() {
    scoreElement.textContent = score;
    compoundsBuiltElement.textContent = compoundsBuilt;
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
