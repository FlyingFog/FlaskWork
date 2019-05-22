from flask import Blueprint, render_template, redirect, url_for, flash,request

blue = Blueprint("first" ,__name__)


@blue.route('/')
def main():
    return "hello"

