#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->OGLayout->addWidget(new OGLWidget(parent));
}

MainWindow::~MainWindow()
{
    delete ui;
}
