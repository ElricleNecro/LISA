#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow), glw(new OGLWidget(0, parent))
{
    ui->setupUi(this);
    ui->OGLayout->addWidget(glw);
    glw->updateGL();
}

MainWindow::~MainWindow()
{
    delete ui;
    delete glw;
}
