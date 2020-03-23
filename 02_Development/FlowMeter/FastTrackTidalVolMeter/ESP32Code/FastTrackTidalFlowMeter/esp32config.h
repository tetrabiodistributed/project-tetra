/*
Copyright (c) 2020 Mechatroniks
This software is licensed under the MIT License. See the license file for details.
Source: github.com/mechatroniks-git
*/

#ifndef __ESP32CONFIG_H__
#define __ESP32CONFIG_H__

// Digital Pins
    constexpr gpio_num_t  esp32I2CSCL    {GPIO_NUM_0};
    constexpr gpio_num_t  esp32USBTx     {GPIO_NUM_1};
    constexpr gpio_num_t  esp32SDData    {GPIO_NUM_2};
    constexpr gpio_num_t  esp32USBRx     {GPIO_NUM_3};
    constexpr gpio_num_t  esp32I2CSDA    {GPIO_NUM_4};
    constexpr gpio_num_t  esp32Uart2Tx   {GPIO_NUM_5};
    constexpr gpio_num_t  esp32SpiClk    {GPIO_NUM_6};
    constexpr gpio_num_t  esp32SpiQ      {GPIO_NUM_7};
    constexpr gpio_num_t  esp32SpiD      {GPIO_NUM_8};
    constexpr gpio_num_t  esp32SpiHd     {GPIO_NUM_9};
    constexpr gpio_num_t  esp32SpiWp     {GPIO_NUM_10};
    constexpr gpio_num_t  esp32SpiCs0    {GPIO_NUM_11};
    constexpr gpio_num_t  esp32EthPhyPwr {GPIO_NUM_12};
    constexpr gpio_num_t  esp32Led       {GPIO_NUM_13};
    constexpr gpio_num_t  esp32SDClk     {GPIO_NUM_14};
    constexpr gpio_num_t  esp32SDCmd     {GPIO_NUM_15};
    constexpr gpio_num_t  esp32Uart2Rx   {GPIO_NUM_16};
    constexpr gpio_num_t  esp32EthClk    {GPIO_NUM_17};
    constexpr gpio_num_t  esp32EthMdio   {GPIO_NUM_18};
    constexpr gpio_num_t  esp32EthTxD0   {GPIO_NUM_19};
//  constexpr gpio_num_t                 {GPIO_NUM_20};
    constexpr gpio_num_t  esp32EthTxEn   {GPIO_NUM_21};
    constexpr gpio_num_t  esp32EthTxD1   {GPIO_NUM_22};
    constexpr gpio_num_t  esp32EthMDC    {GPIO_NUM_23};
//  constexpr gpio_num_t                 {GPIO_NUM_24};
    constexpr gpio_num_t  esp32EthRxD0   {GPIO_NUM_25};
    constexpr gpio_num_t  esp32EthRxD1   {GPIO_NUM_26};
    constexpr gpio_num_t  esp32EthRxCrs  {GPIO_NUM_27};
//  constexpr gpio_num_t                 {GPIO_NUM_28};
//  constexpr gpio_num_t                 {GPIO_NUM_29};
//  constexpr gpio_num_t                 {GPIO_NUM_30};
//  constexpr gpio_num_t                 {GPIO_NUM_31};
    constexpr gpio_num_t  esp32CanTx     {GPIO_NUM_32};
    constexpr gpio_num_t  esp32CanRx     {GPIO_NUM_33};
    constexpr gpio_num_t  esp32But1      {GPIO_NUM_34};
    constexpr gpio_num_t  esp32ADCBat    {GPIO_NUM_35};
//  constexpr gpio_num_t  NC             {GPIO_NUM_36};
//  constexpr gpio_num_t                 {GPIO_NUM_37};
//  constexpr gpio_num_t                 {GPIO_NUM_38};
    constexpr gpio_num_t  esp32ADCExtPwr {GPIO_NUM_39};





#endif
