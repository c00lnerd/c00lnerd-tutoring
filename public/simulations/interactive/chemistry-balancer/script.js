let currentStep = 1;
const totalSteps = 4;

function nextStep() {
    if (currentStep < totalSteps) {
        document.getElementById(`step${currentStep}`).classList.remove('active');
        currentStep++;
        document.getElementById(`step${currentStep}`).classList.add('active');
    }
}

function previousStep() {
    if (currentStep > 1) {
        document.getElementById(`step${currentStep}`).classList.remove('active');
        currentStep--;
        document.getElementById(`step${currentStep}`).classList.add('active');
    }
}

function resetSteps() {
    document.getElementById(`step${currentStep}`).classList.remove('active');
    currentStep = 1;
    document.getElementById('step1').classList.add('active');
}

function toggleDetails(stepNumber) {
    const detailsPanel = document.getElementById(`details${stepNumber}`);
    const button = document.querySelector(`#step${stepNumber} .details-btn`);
    if (detailsPanel.classList.contains('show')) {
        detailsPanel.classList.remove('show');
        button.textContent = 'Show More Details';
    } else {
        detailsPanel.classList.add('show');
        button.textContent = 'Hide Details';
    }
}

function addNavigationButtons(stepId) {
    const step = document.getElementById(`step${stepId}`);
    const explanation = document.getElementById(`step${stepId}Explanation`);
    
    // Add details button if not already present
    if (!explanation.querySelector('.details-btn')) {
        const detailsButton = document.createElement('button');
        detailsButton.className = 'details-btn';
        detailsButton.onclick = () => toggleDetails(stepId);
        detailsButton.textContent = 'Show More Details';
        explanation.appendChild(detailsButton);
        
        const detailsPanel = document.createElement('div');
        detailsPanel.className = 'details-panel';
        detailsPanel.id = `details${stepId}`;
        explanation.appendChild(detailsPanel);
    }
    
    // Add navigation buttons
    const existingNav = step.querySelector('.nav-buttons');
    if (existingNav) {
        existingNav.remove();
    }
    
    const navDiv = document.createElement('div');
    navDiv.className = 'nav-buttons';
    navDiv.style = 'margin-top: 20px; display: flex; gap: 10px;';
    
    if (stepId > 1) {
        const prevButton = document.createElement('button');
        prevButton.className = 'btn btn-primary';
        prevButton.onclick = previousStep;
        prevButton.textContent = 'Previous Step';
        navDiv.appendChild(prevButton);
    }
    
    if (stepId < totalSteps) {
        const nextButton = document.createElement('button');
        nextButton.className = 'btn btn-primary';
        nextButton.onclick = nextStep;
        nextButton.textContent = 'Next Step';
        navDiv.appendChild(nextButton);
    } else {
        const resetButton = document.createElement('button');
        resetButton.className = 'btn btn-primary';
        resetButton.onclick = resetSteps;
        resetButton.textContent = 'Start Over';
        navDiv.appendChild(resetButton);
    }
    
    step.appendChild(navDiv);
}

const reactionTypes = {
    precipitation: {
        steps: ['Identify reactants and products', 'Write complete ionic equation', 'Identify spectator ions', 'Write net ionic equation'],
        details: {
            1: 'Focus on solubility rules and precipitate formation',
            2: 'Break down aqueous compounds into ions',
            3: 'Look for unchanged ions',
            4: 'Show only reacting species'
        }
    },
    redox: {
        steps: ['Identify oxidation states', 'Separate half-reactions', 'Balance atoms and charges', 'Combine half-reactions'],
        details: {
            1: 'Calculate oxidation numbers for each atom',
            2: 'Write oxidation and reduction half-reactions',
            3: 'Add H⁺, OH⁻, or H₂O to balance',
            4: 'Multiply half-reactions to equalize electrons'
        }
    },
    acid_base: {
        steps: ['Identify acid and base', 'Write molecular equation', 'Write ionic equation', 'Identify products'],
        details: {
            1: 'Identify H⁺ donors and acceptors',
            2: 'Show complete molecular formula',
            3: 'Break down into ions where applicable',
            4: 'Focus on H⁺ and OH⁻ combination'
        }
    },
    gas_forming: {
        steps: ['Identify gas product', 'Write molecular equation', 'Balance equation', 'Check gas evolution'],
        details: {
            1: 'Look for common gases (CO₂, H₂S, NH₃)',
            2: 'Write complete formula equation',
            3: 'Balance atoms on both sides',
            4: 'Verify gas formation conditions'
        }
    }
};

const examples = {
    // Precipitation Reactions
    na2so4: {
        type: 'precipitation',
        molecular: "Na₂SO₄(aq) + BaCl₂(aq) → 2NaCl(aq) + BaSO₄(s)",
        complete_ionic: "2Na⁺ + SO₄²⁻ + Ba²⁺ + 2Cl⁻ → 2Na⁺ + 2Cl⁻ + BaSO₄(s)",
        spectators: ["Na⁺", "Cl⁻"],
        net_ionic: "Ba²⁺ + SO₄²⁻ → BaSO₄(s)",
        explanation: "Sodium sulfate and barium chloride form insoluble barium sulfate precipitate."
    },
    agno3: {
        type: 'precipitation',
        molecular: "AgNO₃(aq) + NaCl(aq) → AgCl(s) + NaNO₃(aq)",
        complete_ionic: "Ag⁺ + NO₃⁻ + Na⁺ + Cl⁻ → AgCl(s) + Na⁺ + NO₃⁻",
        spectators: ["Na⁺", "NO₃⁻"],
        net_ionic: "Ag⁺ + Cl⁻ → AgCl(s)",
        explanation: "This reaction forms insoluble silver chloride precipitate."
    },
    // Redox Reactions
    permanganate: {
        type: 'redox',
        molecular: "2KMnO₄ + 5H₂C₂O₄ + 3H₂SO₄ → 2MnSO₄ + 10CO₂ + K₂SO₄ + 8H₂O",
        oxidation_numbers: {
            'Mn': '+7 → +2',
            'C': '+3 → +4'
        },
        half_reactions: [
            "MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O (reduction)",
            "C₂O₄²⁻ → 2CO₂ + 2e⁻ (oxidation)"
        ],
        balanced: "2MnO₄⁻ + 16H⁺ + 5C₂O₄²⁻ → 2Mn²⁺ + 10CO₂ + 8H₂O",
        explanation: "Permanganate oxidizes oxalate to CO₂, while Mn(VII) is reduced to Mn(II)"
    },
    fe_cu: {
        type: 'redox',
        molecular: "Fe(s) + CuSO₄(aq) → FeSO₄(aq) + Cu(s)",
        complete_ionic: "Fe(s) + Cu²⁺ + SO₄²⁻ → Fe²⁺ + SO₄²⁻ + Cu(s)",
        oxidation_numbers: {
            'Fe': '0 → +2',
            'Cu': '+2 → 0'
        },
        half_reactions: [
            "Fe → Fe²⁺ + 2e⁻",
            "Cu²⁺ + 2e⁻ → Cu"
        ],
        balanced: "Fe(s) + Cu²⁺ → Fe²⁺ + Cu(s)",
        explanation: "Iron metal reduces copper(II) ions to copper metal"
    },
    zn_acid: {
        type: 'redox',
        molecular: "Zn(s) + 2HCl(aq) → ZnCl₂(aq) + H₂(g)",
        complete_ionic: "Zn(s) + 2H⁺ + 2Cl⁻ → Zn²⁺ + 2Cl⁻ + H₂(g)",
        oxidation_numbers: {
            'Zn': '0 → +2',
            'H': '+1 → 0'
        },
        half_reactions: [
            "Zn(s) → Zn²⁺ + 2e⁻",
            "2H⁺ + 2e⁻ → H₂(g)"
        ],
        balanced: "Zn(s) + 2H⁺ → Zn²⁺ + H₂(g)",
        explanation: "Zinc metal is oxidized to Zn²⁺ while H⁺ ions are reduced to H₂ gas"
    },
    // Acid-Base Reactions
    hcl_naoh: {
        type: 'acid_base',
        molecular: "HCl(aq) + NaOH(aq) → NaCl(aq) + H₂O(l)",
        acid_base_id: {
            acid: 'HCl (donates H⁺)',
            base: 'OH⁻ (accepts H⁺)'
        },
        ionic: "H⁺ + Cl⁻ + Na⁺ + OH⁻ → Na⁺ + Cl⁻ + H₂O",
        spectators: ["Na⁺", "Cl⁻"],
        net_ionic: "H⁺ + OH⁻ → H₂O",
        explanation: "Simple neutralization: H⁺ and OH⁻ combine to form water, while Na⁺ and Cl⁻ are spectator ions",
        ph_change: "pH increases as H⁺ is consumed"
    },
    h2so4_ba: {
        type: 'acid_base',
        molecular: "H₂SO₄(aq) + Ba(OH)₂(aq) → BaSO₄(s) + 2H₂O(l)",
        acid_base_id: {
            acid: 'H₂SO₄ (donates 2H⁺)',
            base: 'OH⁻ (accepts H⁺)'
        },
        ionic: "2H⁺ + SO₄²⁻ + Ba²⁺ + 2OH⁻ → BaSO₄(s) + 2H₂O",
        net_ionic: "SO₄²⁻ + Ba²⁺ → BaSO₄(s)",
        neutralization: "2H⁺ + 2OH⁻ → 2H₂O",
        explanation: "Two simultaneous reactions occur:\n1. Precipitation: SO₄²⁻ + Ba²⁺ → BaSO₄(s)\n2. Neutralization: 2H⁺ + 2OH⁻ → 2H₂O",
        ph_change: "pH increases as H⁺ is consumed"
    },
    carbonic: {
        type: 'acid_base',
        molecular: "2HCl(aq) + Na₂CO₃(aq) → 2NaCl(aq) + H₂O(l) + CO₂(g)",
        acid_base_id: {
            acid: 'HCl (strong acid)',
            base: 'CO₃²⁻ (weak base)'
        },
        ionic: "2H⁺ + 2Cl⁻ + 2Na⁺ + CO₃²⁻ → 2Na⁺ + 2Cl⁻ + H₂O + CO₂",
        net_ionic: "2H⁺ + CO₃²⁻ → H₂O + CO₂",
        explanation: "Acid-base reaction with gas evolution",
        ph_change: "pH increases slightly as H⁺ is consumed"
    },
    // Gas-Forming Reactions
    carbonate: {
        type: 'gas_forming',
        molecular: "CaCO₃(s) + 2HCl(aq) → CaCl₂(aq) + H₂O(l) + CO₂(g)",
        gas_properties: {
            formula: 'CO₂',
            name: 'Carbon dioxide',
            test: 'Turns limewater milky'
        },
        ionic: "CaCO₃(s) + 2H⁺ + 2Cl⁻ → Ca²⁺ + 2Cl⁻ + H₂O + CO₂(g)",
        net: "CaCO₃(s) + 2H⁺ → Ca²⁺ + H₂O + CO₂(g)",
        explanation: "Carbonate decomposition with CO₂ evolution"
    },
    sulfide: {
        type: 'gas_forming',
        molecular: "FeS(s) + 2HCl(aq) → FeCl₂(aq) + H₂S(g)",
        gas_properties: {
            formula: 'H₂S',
            name: 'Hydrogen sulfide',
            test: 'Rotten egg smell, blackens lead acetate paper'
        },
        ionic: "FeS(s) + 2H⁺ + 2Cl⁻ → Fe²⁺ + 2Cl⁻ + H₂S(g)",
        net: "FeS(s) + 2H⁺ → Fe²⁺ + H₂S(g)",
        explanation: "Metal sulfide reaction producing H₂S gas"
    },
    ammonia: {
        type: 'gas_forming',
        molecular: "NH₄Cl(s) + NaOH(aq) → NaCl(aq) + H₂O(l) + NH₃(g)",
        gas_properties: {
            formula: 'NH₃',
            name: 'Ammonia',
            test: 'Pungent smell, turns red litmus blue'
        },
        ionic: "NH₄⁺ + Cl⁻ + Na⁺ + OH⁻ → Na⁺ + Cl⁻ + H₂O + NH₃(g)",
        net: "NH₄⁺ + OH⁻ → H₂O + NH₃(g)",
        explanation: "Ammonium salt decomposition producing NH₃ gas"
    },
    pb2no3: {
        type: 'precipitation',
        molecular: "Pb(NO₃)₂(aq) + 2KI(aq) → PbI₂(s) + 2KNO₃(aq)",
        complete_ionic: "Pb²⁺ + 2NO₃⁻ + 2K⁺ + 2I⁻ → PbI₂(s) + 2K⁺ + 2NO₃⁻",
        spectators: ["K⁺", "NO₃⁻"],
        net_ionic: "Pb²⁺ + 2I⁻ → PbI₂(s)",
        explanation: "This reaction forms insoluble lead(II) iodide precipitate."
    }
};

function changeReactionType() {
    const selectedType = document.getElementById('reactionTypeSelect').value;
    const equationSelect = document.getElementById('equationSelect');
    
    // Remove all show-* classes
    equationSelect.className = '';
    // Add appropriate show class
    equationSelect.classList.add(`show-${selectedType}`);
    
    // Update steps based on reaction type
    const steps = reactionTypes[selectedType].steps;
    updateStepTitles(steps);
    
    // Select first option in the equations list
    const firstOption = equationSelect.querySelector(`.${selectedType}`);
    if (firstOption) {
        equationSelect.value = firstOption.value;
        // Get the example and update content
        const example = examples[firstOption.value];
        updateContent(example);
    }

    // Update explanations based on reaction type
    updateExplanationsForType(selectedType);
}

function updateStepTitles(steps) {
    steps.forEach((step, index) => {
        const stepElement = document.getElementById(`step${index + 1}`);
        if (stepElement) {
            const titleElement = stepElement.querySelector('h3');
            if (titleElement) {
                titleElement.textContent = `Step ${index + 1}: ${step}`;
            }
        }
    });
}

function updateContent(example) {
    document.getElementById('molecularEquation').textContent = example.molecular;

    // Store current step before hiding
    const previousStep = currentStep;

    // Hide all steps first
    for (let i = 1; i <= totalSteps; i++) {
        document.getElementById(`step${i}`).classList.remove('active');
    }

    // Update content based on reaction type
    switch(example.type) {
        case 'precipitation':
            updatePrecipitationExample(example);
            break;
        case 'redox':
            updateRedoxExample(example);
            break;
        case 'acid_base':
            updateAcidBaseExample(example);
            break;
        case 'gas_forming':
            updateGasFormingExample(example);
            break;
    }

    // Add navigation buttons to all steps
    for (let i = 1; i <= totalSteps; i++) {
        addNavigationButtons(i);
    }

    // Show the same step that was active before
    document.getElementById(`step${previousStep}`).classList.add('active');
}

function changeExample() {
    const example = examples[document.getElementById('equationSelect').value];
    updateContent(example);
}

function updatePrecipitationExample(example) {
    // Step 1: Show molecular equation
    document.getElementById('step1Explanation').innerHTML = 
        `<p>The molecular equation shows all compounds in their undissociated form:</p>
         <div class="equation">${example.molecular}</div>
         <div class="details-panel" id="details1">
            <h4>Understanding Molecular Equations:</h4>
            <ul>
                <li>Shows complete formulas of all compounds</li>
                <li>Includes state symbols (aq, s, l, g)</li>
                <li>Does not show individual ions</li>
            </ul>
         </div>`;

    // Step 2: Show complete ionic equation
    document.getElementById('step2Explanation').innerHTML = 
        `<p>The complete ionic equation shows all dissociated ions:</p>
         <div class="equation">${example.complete_ionic}</div>
         <div class="details-panel" id="details2">
            <h4>Complete Ionic Equations:</h4>
            <ul>
                <li>Show all aqueous compounds as separated ions</li>
                <li>Keep solid, liquid, and gas compounds together</li>
                <li>Include all ions present in solution</li>
            </ul>
         </div>`;

    // Step 3: Identify spectator ions
    const reactionProducts = example.net_ionic.split('→')[1].trim();
    const product = reactionProducts.match(/[A-Za-z₀-₉⁺⁻(]+/)[0];
    const reactants = example.net_ionic.split('→')[0].trim().split('+').map(r => r.trim());
    
    document.getElementById('step3Explanation').innerHTML = 
        `<p>Look for ions that appear unchanged on both sides:</p>
         <div class="equation" style="font-size: 1.2em; margin: 15px 0;">
            <strong>${example.complete_ionic}</strong>
         </div>
         <div class="explanation">
            <ul>
                ${example.spectators.map(ion => `<li>${ion} appears on both sides (spectator ion)</li>`).join('')}
                <li>${reactants.join(' and ')} combine to form ${product} (reacting ions)</li>
            </ul>
         </div>
         <div class="details-panel" id="details3">
            <h4>Understanding Spectator Ions:</h4>
            <ul>
                <li>Spectator ions do not participate in the reaction</li>
                <li>They remain unchanged throughout the process</li>
                <li>They appear in the same form on both sides of the equation</li>
                <li>Removing them simplifies the equation to show only the actual reaction</li>
            </ul>
            <h4>Why Remove Spectator Ions?</h4>
            <p>Removing spectator ions helps us:</p>
            <ul>
                <li>Focus on the actual chemical change</li>
                <li>Identify the driving force of the reaction</li>
                <li>Understand precipitation reactions better</li>
                <li>Write simpler, more meaningful equations</li>
            </ul>
         </div>`;

    // Step 4: Show net ionic equation
    document.getElementById('step4Explanation').innerHTML = 
        `<p>Net ionic equation (after removing spectator ions):</p>
         <div class="equation">${example.net_ionic}</div>
         <p><strong>Explanation:</strong> ${example.explanation}</p>
         <div class="details-panel" id="details4">
            <h4>Net Ionic Equations:</h4>
            <ul>
                <li>Show only the ions and compounds that participate in the reaction</li>
                <li>Exclude spectator ions</li>
                <li>Represent the actual chemical change</li>
                <li>Are the same for similar precipitation reactions</li>
            </ul>
         </div>`;
}

function updateRedoxExample(example) {
    // Step 1: Identify oxidation states
    const oxidationElements = Object.entries(example.oxidation_numbers)
        .map(([element, change]) => `<li>${element}: ${change}</li>`)
        .join('');

    document.getElementById('step1Explanation').innerHTML = 
        `<p>First, let's identify the oxidation states of each element:</p>
         <div class="equation">${example.molecular}</div>
         <div class="oxidation-states">
            <h4>Oxidation States:</h4>
            <ul>${oxidationElements}</ul>
         </div>
         <div class="details-panel" id="details1">
            <h4>Rules for Assigning Oxidation Numbers:</h4>
            <ul>
                <li>Free elements have oxidation number of 0</li>
                <li>Simple ions: charge on the ion</li>
                <li>Group 1 metals: +1 in compounds</li>
                <li>Group 2 metals: +2 in compounds</li>
                <li>Hydrogen: +1 (usually) or -1 (metal hydrides)</li>
                <li>Oxygen: -2 (usually) or -1 (peroxides)</li>
            </ul>
         </div>`;

    // Step 2: Show half-reactions
    const oxidationElement = Object.entries(example.oxidation_numbers)[0];
    const reductionElement = Object.entries(example.oxidation_numbers)[1];

    document.getElementById('step2Explanation').innerHTML = 
        `<div class="equation">
            <p>Complete ionic equation:</p>
            <div>${example.complete_ionic}</div>
         </div>
         <div class="equation">
            <p>Oxidation half-reaction (loss of electrons):</p>
            <div>${example.half_reactions[0]}</div>
            <p>Reduction half-reaction (gain of electrons):</p>
            <div>${example.half_reactions[1]}</div>
         </div>
         <div class="details-panel" id="details2">
            <h4>Oxidation Number Changes:</h4>
            <ul>
                <li>Oxidation (${oxidationElement[0]}: ${oxidationElement[1]}): Loss of electrons</li>
                <li>Reduction (${reductionElement[0]}: ${reductionElement[1]}): Gain of electrons</li>
            </ul>
            <h4>Understanding Half-Reactions:</h4>
            <ul>
                <li>Oxidation involves loss of electrons (increase in oxidation number)</li>
                <li>Reduction involves gain of electrons (decrease in oxidation number)</li>
                <li>The number of electrons lost equals the number gained</li>
                <li>Combined balanced equation: ${example.balanced}</li>
            </ul>
         </div>
         </div>`;

    // Step 3: Balance atoms and charges
    document.getElementById('step3Explanation').innerHTML = 
        `<p>Balance each half-reaction:</p>
         <div class="equation">
            ${example.half_reactions.map(reaction => 
                `<div>${reaction}</div>`
            ).join('')}
         </div>
         <div class="details-panel" id="details3">
            <h4>Balancing Steps:</h4>
            <ol>
                <li>Balance atoms other than H and O</li>
                <li>Balance O atoms by adding H₂O</li>
                <li>Balance H atoms by adding H⁺</li>
                <li>Balance charge by adding electrons</li>
            </ol>
         </div>
         </div>`;

    // Step 4: Show final balanced equation
    document.getElementById('step4Explanation').innerHTML = 
        `<p>Final balanced equation:</p>
         <div class="equation">${example.balanced}</div>
         <p><strong>Explanation:</strong> ${example.explanation}</p>
         <div class="details-panel" id="details4">
            <h4>Final Checks:</h4>
            <ul>
                <li>All atoms are balanced on both sides</li>
                <li>Total charge is equal on both sides</li>
                <li>Electrons transferred match in both half-reactions</li>
                <li>State symbols are correct (s, l, g, aq)</li>
            </ul>
            <h4>Common Oxidizing Agents:</h4>
            <ul>
                <li>MnO₄⁻ (permanganate)</li>
                <li>Cr₂O₇²⁻ (dichromate)</li>
                <li>H₂O₂ (hydrogen peroxide)</li>
                <li>O₂ (oxygen)</li>
            </ul>
            <h4>Common Reducing Agents:</h4>
            <ul>
                <li>Active metals (Na, Mg, Al, Zn, Fe)</li>
                <li>H₂ (hydrogen gas)</li>
                <li>CO (carbon monoxide)</li>
                <li>SO₂ (sulfur dioxide)</li>
            </ul>
         </div>
         </div>`;
}

function updateAcidBaseExample(example) {
    // Step 1: Identify acid and base
    document.getElementById('step1Explanation').innerHTML = 
        `<p>First, let's identify the acid and base components:</p>
         <div class="acid-base-info">
            <h4>Reactants:</h4>
            <ul>
                <li>Acid: ${example.acid_base_id.acid}</li>
                <li>Base: ${example.acid_base_id.base}</li>
            </ul>
         </div>
         <div class="equation">${example.molecular}</div>
         <div class="details-panel" id="details1">
            <h4>Acid-Base Properties:</h4>
            <ul>
                <li>Acids donate H⁺ (protons)</li>
                <li>Bases accept H⁺ or provide OH⁻</li>
                <li>Strong acids/bases dissociate completely</li>
                <li>Weak acids/bases dissociate partially</li>
            </ul>
            <h4>Common Strong Acids:</h4>
            <ul>
                <li>HCl - Hydrochloric acid</li>
                <li>H₂SO₄ - Sulfuric acid</li>
                <li>HNO₃ - Nitric acid</li>
            </ul>
            <h4>Common Strong Bases:</h4>
            <ul>
                <li>NaOH - Sodium hydroxide</li>
                <li>KOH - Potassium hydroxide</li>
                <li>Ca(OH)₂ - Calcium hydroxide</li>
            </ul>
         </div>`;

    // Step 2: Show molecular equation
    document.getElementById('step2Explanation').innerHTML = 
        `<p>The molecular equation shows the complete reaction:</p>
         <div class="equation">${example.molecular}</div>
         <div class="details-panel" id="details2">
            <h4>Understanding Acid-Base Reactions:</h4>
            <ul>
                <li>Acid + Base → Salt + Water</li>
                <li>This is called a neutralization reaction</li>
                <li>The pH moves toward 7 (neutral)</li>
                <li>Heat is often released (exothermic)</li>
            </ul>
            <h4>Indicators:</h4>
            <ul>
                <li>Litmus: Red in acid, blue in base</li>
                <li>Phenolphthalein: Clear in acid, pink in base</li>
                <li>Universal: Different colors for different pH</li>
            </ul>
         </div>`;

    // Step 3: Show ionic equation
    document.getElementById('step3Explanation').innerHTML = 
        `<p>The complete ionic equation shows all ions:</p>
         <div class="equation">${example.ionic || 'H⁺ + Cl⁻ + Na⁺ + OH⁻ → Na⁺ + Cl⁻ + H₂O'}</div>
         <div class="explanation">
            <p>Identify the ions:</p>
            <ul>
                <li>Na⁺ appears on both sides (spectator ion)</li>
                <li>Cl⁻ appears on both sides (spectator ion)</li>
                <li>H⁺ and OH⁻ combine to form H₂O (reacting ions)</li>
            </ul>
            <p>pH change: ${example.ph_change}</p>
         </div>
         <div class="details-panel" id="details3">
            <h4>Complete Ionic Equations:</h4>
            <ul>
                <li>Show all ions present in solution</li>
                <li>Help identify spectator ions</li>
                <li>Include state symbols (aq, l, s, g)</li>
                <li>Show all species present</li>
            </ul>
            <h4>pH Scale:</h4>
            <ul>
                <li>pH < 7: Acidic solution</li>
                <li>pH = 7: Neutral solution</li>
                <li>pH > 7: Basic solution</li>
            </ul>
         </div>`;

    // Step 4: Show net ionic equation
    document.getElementById('step4Explanation').innerHTML = 
        `<p>The net ionic equation shows the essential reaction:</p>
         <div class="equation">${example.net_ionic || 'H⁺ + OH⁻ → H₂O'}</div>
         <p><strong>Explanation:</strong> ${example.explanation}</p>
         <div class="details-panel" id="details4">
            <h4>Net Ionic Equations:</h4>
            <ul>
                <li>Shows only reacting species (H⁺ and OH⁻)</li>
                <li>Omits spectator ions (Na⁺, Cl⁻)</li>
                <li>Same for all strong acid-base reactions</li>
                <li>Always produces water (H₂O)</li>
            </ul>
            <h4>Neutralization Products:</h4>
            <ul>
                <li>Water (H₂O) is always formed</li>
                <li>A salt is also produced (e.g., NaCl)</li>
                <li>Solution becomes neutral (pH ≈ 7)</li>
                <li>Heat is released (exothermic)</li>
            </ul>
         </div>`;
}

function updateGasFormingExample(example) {
    // Step 1: Identify gas product
    document.getElementById('step1Explanation').innerHTML = 
        `<p>First, let's identify the gas product and its properties:</p>
         <div class="gas-info">
            <h4>Gas Product: ${example.gas_properties.name} (${example.gas_properties.formula})</h4>
            <p>Detection Test: ${example.gas_properties.test}</p>
         </div>
         <div class="equation">${example.molecular}</div>
         <div class="details-panel" id="details1">
            <h4>Common Gas-Forming Reactions:</h4>
            <ul>
                <li>Carbonates + Acids → CO₂ gas</li>
                <li>Metal + Acid → H₂ gas</li>
                <li>Sulfites + Acids → SO₂ gas</li>
                <li>NH₄⁺ + OH⁻ → NH₃ gas</li>
            </ul>
            <h4>Gas Tests:</h4>
            <ul>
                <li>CO₂: Turns limewater milky</li>
                <li>H₂: "Pop" test with flame</li>
                <li>NH₃: White fumes with HCl</li>
                <li>SO₂: Bleaches wet litmus</li>
            </ul>
         </div>`;

    // Step 2: Show molecular equation
    document.getElementById('step2Explanation').innerHTML = 
        `<p>The molecular equation shows all compounds before dissociation:</p>
         <div class="equation">${example.molecular}</div>
         <div class="details-panel" id="details2">
            <h4>Understanding Molecular Equations:</h4>
            <ul>
                <li>Shows complete formulas of all compounds</li>
                <li>Includes state symbols (s, l, g, aq)</li>
                <li>Helps visualize the reactants and products</li>
                <li>Does not show individual ions</li>
            </ul>
         </div>`;

    // Step 3: Show ionic equation
    document.getElementById('step3Explanation').innerHTML = 
        `<p>The complete ionic equation shows dissociated ions:</p>
         <div class="equation">${example.ionic}</div>
         <div class="details-panel" id="details3">
            <h4>Complete Ionic Equations:</h4>
            <ul>
                <li>Show all aqueous compounds as separated ions</li>
                <li>Keep solid, liquid, and gas compounds together</li>
                <li>Include all ions present in solution</li>
                <li>Help identify spectator ions</li>
            </ul>
         </div>`;

    // Step 4: Show net equation
    document.getElementById('step4Explanation').innerHTML = 
        `<p>The net ionic equation shows the actual reaction:</p>
         <div class="equation">${example.net}</div>
         <p><strong>Explanation:</strong> ${example.explanation}</p>
         <div class="details-panel" id="details4">
            <h4>Net Ionic Equations:</h4>
            <ul>
                <li>Show only species that participate in the reaction</li>
                <li>Omit spectator ions</li>
                <li>Represent the actual chemical change</li>
                <li>Are the same for similar gas-forming reactions</li>
            </ul>
         </div>`;
}

function toggleDetails(step) {
    const detailsPanel = document.getElementById(`details${step}`);
    if (detailsPanel.classList.contains('show')) {
        detailsPanel.classList.remove('show');
    } else {
        detailsPanel.classList.add('show');
    }
}

function nextStep() {
    if (currentStep < totalSteps) {
        const currentStepEl = document.getElementById(`step${currentStep}`);
        const nextStepEl = document.getElementById(`step${currentStep + 1}`);
        if (currentStepEl && nextStepEl) {
            currentStepEl.classList.remove('active');
            currentStep++;
            nextStepEl.classList.add('active');
        }
    }
}

function previousStep() {
    if (currentStep > 1) {
        const currentStepEl = document.getElementById(`step${currentStep}`);
        const prevStepEl = document.getElementById(`step${currentStep - 1}`);
        if (currentStepEl && prevStepEl) {
            currentStepEl.classList.remove('active');
            currentStep--;
            prevStepEl.classList.add('active');
        }
    }
}

function resetSteps() {
    document.getElementById(`step${currentStep}`).classList.remove('active');
    currentStep = 1;
    document.getElementById(`step${currentStep}`).classList.add('active');
}

function toggleDetails(step) {
    const detailsPanel = document.getElementById(`details${step}`);
    if (detailsPanel) {
        detailsPanel.classList.toggle('show');
        const btn = event.target;
        btn.textContent = detailsPanel.classList.contains('show') ? 'Hide Details' : 'Show More Details';
    }
}

// Initialize the page
window.onload = function() {
    // Initialize reaction type selector
    const reactionTypeSelect = document.getElementById('reactionTypeSelect');
    const equationSelect = document.getElementById('equationSelect');
    
    // Set initial reaction type class
    equationSelect.classList.add(`show-${reactionTypeSelect.value}`);
    
    // Update steps and explanations for initial reaction type
    const initialType = reactionTypeSelect.value;
    updateStepTitles(reactionTypes[initialType].steps);
    updateExplanationsForType(initialType);
    
    // Get the initial example and update content
    const example = examples[equationSelect.value];
    document.getElementById('molecularEquation').textContent = example.molecular;
    
    // Update content based on reaction type
    switch(example.type) {
        case 'precipitation':
            updatePrecipitationExample(example);
            break;
        case 'redox':
            updateRedoxExample(example);
            break;
        case 'acid_base':
            updateAcidBaseExample(example);
            break;
        case 'gas_forming':
            updateGasFormingExample(example);
            break;
    }
    
    // Show first step
    currentStep = 1;
    document.getElementById('step1').classList.add('active');
};
