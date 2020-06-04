---
title: "Project Tetra Overview"
linkTitle: "Project Tetra Overview"
weight: 1
description: >
  Broad overview of project tetra.
---

## Executive Summary

Current medical standard operating procedure requires that patients who become severely ill with COVID-19 be treated using external ventilation.  As the virus spreads, projections suggest that there are not enough ventilators to meet the expected numbers of patients throughout the world.  Project Tetra seeks to create a ventilator splitter so that hospitals inundated with covid-19 patients can effectively increase the number of already available ventilators by up to a factor of 4. The project aims to produce two versions of the device: one that has been approved by the FDA under the Emergency Use Authorization guidance, and an open source model intended to be made with locally sourced materials.

## Introduction

As of May 19, 2020, 5 million cases of coronavirus have been reported worldwide, with over 320,000 deaths attributed to the virus [1].  Initial clinical reports of those infected with the virus indicated that the fatality rate nears 2-3%, but closer inspection of the number of cases shows that up to 5% of patients require ventilation (see Figure 1, the bottom bar):
![Figure 1](./Figure_1.png)

*Figure 1: A breakdown of how individuals react to a COVID-19 infection sourced from March, 2020.  At that point in time, 85% of the infected population appeared to recover without medical intervention, while 5% of the infected population would require invasive ventilation to recover, and up to half of those patients were not surviving.  If that 5% of infected individuals do not receive ventilation, then the entire group is at serious risk of death.[2]*

Patients who require ventilation will die without it.  If the hospital cannot provide ventilation due to a lack of ventilators, then health care providers will be required to make “god decisions” about which patients live and which patients die [3, 4]. The added stress of these decisions negatively impacts mental health of clinicians treating patients, weakening the support these patients can receive[5].

Several projects already exist that aim to increase the supply of ventilators [6, 7, 8].  Ventilators are complicated devices, however, that require four touchpoints of control for a respiratory therapist or clinician:

  1.  Peak Inspiratory Pressure, or PIP.   This number determines the amount of air in each breath, which clinically should have a maximum value of 40 cm H2O [9].  Most ICU ventilators, for reference, can provide PIP between 100cm H2O and 200cm H2O, or enough PIP for 2-4 intubated patients.
  2. Fraction of Inspired Oxygen, or FiO2.  This number indicates the fraction of oxygen in the air provided in each patient’s breath [10].  Smaller breaths require more oxygen in each breath, but too much oxygen can lead to oxygen toxicity, producing a complicated tradeoff in patient care.
  3. Breath frequency.  A ventilator may be set to 12 breaths per minute, or a breath every 5 seconds, for instance.
  4. Positive End Expiratory Pressure, or PEEP.  This number determines how much pressure is left in the lungs after each breath is taken[11].  If PEEP is reduced to zero, then the lungs effectively collapse between each breath, which can cause long-term scarring in patient tissue.

FDA EUA approved ventilator splitters are far less complicated than a full ventilator. The simplest FDA approved ventilator splitters  provide none of these control points [12, 13].  Because these devices provide no control points, severe complications can arise during the course of their use, as enumerated by the American Society of Anesthesiologists [14].  Since none of these control points are available to the clinician or respiratory therapist, patient lung compliance becomes a serious concern, as does cross-contamination between patients.  

The most serious concern is the death of both patients.  Two patients on the same ventilator may begin recovering at different rates.  As a patient recovers, that patient’s lungs become more compliant, meaning that more air can go into those lungs.  The other patient, who is less healthy, remains with compromised lungs.  With no valves or other flow control mechanisms, pressure in the system will naturally increase in the more compliant lungs, causing that healthier patient’s lungs to become damaged through an increase in PIP.  The less healthy patient, on the other hand, receives less air, and slowly drowns.  Project Tetra aims to address this scenario by providing flow control mechanisms and flow monitoring on the splitter. In this example, if one patient recovers faster than another, the clinician can adjust flow using a Tetra valve for each patient, decreasing PIP for the healthier lungs, and increasing PIP for the less healthy patient. In effect, the Tetra decouples the mechanics of ventilation from the control of ventilation, allowing for the ventilator to control breath frequency, PEEP, and FiO2, while tetra provides control points for individual patient tidal volume.



## How Does It Work?
### Overview

Project Tetra, at its heart, is a set of two splitters with a series of valves and a set of monitoring electronics.  One splitter is termed the ‘inspiratory arm’, as this arm takes the air to be inspired by the patients from the ventilator to the patients.  The other splitter is termed the ‘expiratory arm’, as this complex takes the air expired by patients back to the ventilator.  Between the two complexes is a ‘bias circuit’, a branch with a one-way valve to prevent backflow, that joins the two complexes directly.  This bias circuit is crucial for the operation of the system.

Figure 2 lays out the core components of the device.
![Figure 2](./Figure_2.png)

*Figure 2: High-level schematics of the Tetra system.  Air flows from the ventilator to the inspiratory arm, with separate patients isolated by one-way valves, through flow-control valves and shutoff valves, to the patient.  The expired air travels back through a flow meter, a PEEP valve to ensure the patient still has air pressure in their lungs at the end of the breath, and through another one-way valve back to the ventilator.*

Air travels in the following pathway for a given patient on inspiration:
  1.  From the ventilator
  2.  Through a 1-way valve, to prevent backflow and potential cross-contamination between patients
  3.  Through a flow control valve that allows for linear control of the amount of air going to each patient independently of other patients
  4.  Through a shutoff valve
  5.  Through to the patient for an inspired breath

Expiration follows this pathway:
  1.  From the patient
  2.  Through a shutoff valve
  3.  Through a flow meter to capture the expired breath size of the patient
  4.  Through a one-way valve
  5.  Back to the ventilator

A PEEP valve is not required in the expiratory circuit; patient PEEP should be maintained by the ventilator. Note that using the ventilator to maintain PEEP will require that some level of patient matching be done before placing patients on the ventilator.

### Components

**Tetra Valve***
The Tetra flow control valve and PEEP valves all have an internal layout described in Figure 3.

![Figure 3](./Figure_3.png)
*Figure 3: Tetra Valve components.  Air flows through the left portion of the base, and the valve exerts control through the cap sealing flow with the strength of the spring holding the cap in place.  As the cap is screwed down, the spring creates force to hold the cap down, preventing some amount of flow through the valve.*

The Tetra Valve has several design considerations:
  1.  O-rings on the base of the device for quick attachment and detachment of a replacement valve, should the spring lose compliance
  2.  A post to keep the spring/valve complex in place during valve operation, to prevent slipping of the valves inside the cap, as well as ensure one-way air flow
  3.  Finer threading between the cap and the base to increase control in clinical use.
  4.  A fully specified stainless steel spring to ensure lower inter-part performance variability

The use of a spring provides a linear response in the valve, so that a clinician can adjust the valve and expect that the change will be proportional to the physical change on the device. The Tetra valve goes from fully open to fully closed in a single turn of the cap. The flow rate at each cap position is printed on the valve, so that the clinical user does not have to guess about valve position.

**Shutoff Valve**
The shutoff valves are in the system to allow for easy patient attachment/detachment from the system without causing potential disturbance or infection of other patients on the ventilator.  

**Flow Sensor**
There are three different designs for the flow meter. One is based off of a Sensirion 3300 part[16], which is generally not available as the crisis continues. Another uses calibrated mass air flow (MAF) sensors used as an automotive part, and another uses a custom-built part using a Venturi tube [17]. Each of these three components provide the clinician with knowledge of the size of the expired breath for each patient, which is displayed on a central screen.

**The Display**
The flow sensor prints its results to a screen display built on a Raspberry Pi system. The curve detected from the flow meter has some basic processing done to provide the PIP/PEEP curve, as well as curves representing tidal volume, etc.

## References
1. https://www.worldometers.info/coronavirus/

2. https://twitter.com/drchoueiri/status/1243861887420432384

3. https://www.cbsnews.com/news/coronavirus-doctors-hospitals-life-or-death-decisions-pandemic/

4. https://www.bbc.com/news/world-us-canada-52137160

5. https://www.nytimes.com/2020/04/27/nyregion/new-york-city-doctor-suicide-coronavirus.html

6. https://www.nasa.gov/press-release/nasa-developed-ventilator-authorized-by-fda-for-emergency-use/

7. https://www.reuters.com/article/uk-health-coronavirus-czech-ventilators/czech-team-use-easily-available-parts-to-build-prototype-ventilator-idUKKBN21L1Z6

8. https://armeevent.com/

9. https://en.wikipedia.org/wiki/Peak_inspiratory_pressure

10. https://en.wikipedia.org/wiki/Fraction_of_inspired_oxygen

11. https://en.wikipedia.org/wiki/Positive_end-expiratory_pressure

12. https://hub.jhu.edu/2020/04/02/3d-printed-ventilator-splitters-for-covid-19/

13. https://www.prismahealth.org/vesper/

14. https://www.asahq.org/about-asa/newsroom/news-releases/2020/03/joint-statement-on-multiple-patients-per-ventilator

15. https://www.thingiverse.com/thing:4250354

16. https://www.sensirion.com/en/flow-sensors/mass-flow-meters-for-high-precise-measurement-of-gases/proximal-flow-sensors-sfm3300-autoclavable-washable-or-single-use/

17. https://www.sciencedirect.com/topics/engineering/venturi-tube
