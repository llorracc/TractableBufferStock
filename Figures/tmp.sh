#!/bin/bash

orig=/Volumes/Data/Courses/Choice/LectureNotes/Consumption/Handouts/TractableBufferStock/Code/Mathematica/Examples/TractableBufferStock/Figures

for fig in MPCPathAfterDebtLimRise MPCPathAfterGFall MPCPathAfterGRise MPCPathAfterMhoRise MPCPathAfterThetaDrop MPCPathPlot PhaseDiagramAfterGFallPlot PhaseDiagramDecreaseThetaPlot PhaseDiagramIncreaseGPlot PhaseDiagramIncreaseMhoPlot SOENoStakescPath SOEStakescPathAfterThetaDropPlot TractableBufferStockConsFunc TractableBufferStockGrowthA TractableBufferStockGrowthB TractableBufferStockPhaseDiag TractableBufferStockTarget cGroAfterGFallPlot cGroIncreaseMhoPlot cPathAfterThetaDrop cPathAfterThetaDropAgg mPathAfterThetaDrop; do
    [[ -e ./$fig.svg ]] && rm -Rf ./$fig.svg
    [[ -e $orig/$fig.svg ]] && ln -s $orig/$fig.svg
    echo ''
done

