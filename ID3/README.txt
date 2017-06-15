{\rtf1\ansi\ansicpg950\cocoartf1504\cocoasubrtf830
{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 This problem implement an ID3-like decision-tree learned for classification that read files in the ARFF format.\
\
This problem can handle numeric and nominal attributes.\
\
It can be called from the command line:\
\pard\pardeftab720\partightenfactor0

\fs26 \cf0 \expnd0\expndtw0\kerning0
dt-learn <train-set-file> <test-set-file> m\
where m is a threshold that if there are less than m training instances reaching the node, making a node into a leaf. }