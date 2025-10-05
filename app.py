from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy import func, extract
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///expenses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expenses = db.relationship('Expense', backref='category', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    is_monthly = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'description': self.description,
            'date': self.date.strftime('%Y-%m-%d'),
            'category': self.category.name if self.category else None,
            'is_monthly': self.is_monthly,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

@app.route('/')
def index():
    # Get filter parameters
    date_filter = request.args.get('date', type=str)
    date_from = request.args.get('date_from', type=str)
    date_to = request.args.get('date_to', type=str)
    category_filter = request.args.get('category', type=int)
    selected_categories = request.args.getlist('categories', type=int)
    date_toggle = request.args.get('date_toggle', type=str) == 'on'
    date_range_mode = request.args.get('date_range_mode', type=str) == 'on'
    category_toggle = request.args.get('category_toggle', type=str) == 'on'
    
    # Get dashboard statistics based on current filters
    filtered_query = Expense.query
    
    # Apply category filter only if category toggle is ON (prioritize multi-select over single select)
    if category_toggle:
        if selected_categories:
            filtered_query = filtered_query.filter(Expense.category_id.in_(selected_categories))
        elif category_filter:
            filtered_query = filtered_query.filter(Expense.category_id == category_filter)
    
    # Apply date filter if toggle is ON
    if date_toggle:
        if date_range_mode and date_from and date_to:
            # Date range mode: from-to dates
            try:
                from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
                to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
                filtered_query = filtered_query.filter(
                    Expense.date >= from_date,
                    Expense.date <= to_date
                )
            except ValueError:
                pass
        elif date_filter:
            # Single date mode
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                filtered_query = filtered_query.filter(Expense.date == filter_date)
            except ValueError:
                pass
    
    # Calculate filtered totals
    total_spent = db.session.query(func.sum(Expense.amount)).filter(
        Expense.id.in_(filtered_query.with_entities(Expense.id))
    ).scalar() or 0
    
    # For monthly expenses, show filtered total or current month
    if date_toggle and (date_filter or (date_range_mode and date_from and date_to)):
        # When exact date or date range is selected, show that total
        month_spent = total_spent
    else:
        # Get current month expenses with category filter if applied
        current_month = datetime.now().month
        current_year = datetime.now().year
        month_query = db.session.query(func.sum(Expense.amount)).filter(
            extract('year', Expense.date) == current_year,
            extract('month', Expense.date) == current_month
        )
        if category_toggle:
            if selected_categories:
                month_query = month_query.filter(Expense.category_id.in_(selected_categories))
            elif category_filter:
                month_query = month_query.filter(Expense.category_id == category_filter)
        month_spent = month_query.scalar() or 0
    
    # Get total expense count based on filters
    total_expenses = filtered_query.count()
    
    # Get recent expenses with filtering
    recent_query = Expense.query
    
    # Apply date filter - only if toggle is ON
    if date_toggle:
        if date_range_mode and date_from and date_to:
            # Date range mode: from-to dates
            try:
                from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
                to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
                recent_query = recent_query.filter(
                    Expense.date >= from_date,
                    Expense.date <= to_date
                )
            except ValueError:
                pass
        elif date_filter:
            # Single date mode
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                recent_query = recent_query.filter(Expense.date == filter_date)
            except ValueError:
                pass
    
    # Apply category filter only if category toggle is ON
    if category_toggle:
        if selected_categories:
            recent_query = recent_query.filter(Expense.category_id.in_(selected_categories))
        elif category_filter:
            recent_query = recent_query.filter(Expense.category_id == category_filter)
    
    recent_expenses = recent_query.order_by(Expense.date.desc()).limit(5).all()
    
    # Get all categories for filter dropdown
    categories = Category.query.all()
    
    return render_template('index.html', 
                         total_spent=total_spent,
                         month_spent=month_spent,
                         total_expenses=total_expenses,
                         recent_expenses=recent_expenses,
                         categories=categories,
                         selected_date=date_filter,
                         selected_date_from=date_from,
                         selected_date_to=date_to,
                         selected_category=category_filter,
                         selected_categories=selected_categories,
                         date_toggle_on=date_toggle,
                         date_range_mode_on=date_range_mode,
                         category_toggle_on=category_toggle)

@app.route('/expenses')
def expenses():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    expenses = Expense.query.order_by(Expense.date.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    
    categories = Category.query.all()
    return render_template('expenses.html', expenses=expenses, categories=categories)

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            description = request.form['description'].strip()
            expense_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
            category_id = int(request.form['category_id'])
            is_monthly = 'is_monthly' in request.form
            
            if amount <= 0:
                flash('Amount must be greater than 0', 'error')
                return redirect(url_for('add_expense'))
            
            if not description:
                flash('Description is required', 'error')
                return redirect(url_for('add_expense'))
            
            if expense_date > date.today():
                flash('Date cannot be in the future', 'error')
                return redirect(url_for('add_expense'))
            
            expense = Expense(
                amount=amount,
                description=description,
                date=expense_date,
                category_id=category_id,
                is_monthly=is_monthly
            )
            
            db.session.add(expense)
            db.session.commit()
            flash('Expense added successfully!', 'success')
            return redirect(url_for('expenses'))
            
        except ValueError as e:
            flash('Invalid input. Please check your data.', 'error')
            return redirect(url_for('add_expense'))
        except Exception as e:
            flash('An error occurred while adding the expense.', 'error')
            return redirect(url_for('add_expense'))
    
    categories = Category.query.all()
    return render_template('add_expense.html', categories=categories, today=date.today())

@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            description = request.form['description'].strip()
            expense_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
            category_id = int(request.form['category_id'])
            is_monthly = 'is_monthly' in request.form
            
            if amount <= 0:
                flash('Amount must be greater than 0', 'error')
                return redirect(url_for('edit_expense', expense_id=expense_id))
            
            if not description:
                flash('Description is required', 'error')
                return redirect(url_for('edit_expense', expense_id=expense_id))
            
            if expense_date > date.today():
                flash('Date cannot be in the future', 'error')
                return redirect(url_for('edit_expense', expense_id=expense_id))
            
            expense.amount = amount
            expense.description = description
            expense.date = expense_date
            expense.category_id = category_id
            expense.is_monthly = is_monthly
            expense.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Expense updated successfully!', 'success')
            return redirect(url_for('expenses'))
            
        except ValueError as e:
            flash('Invalid input. Please check your data.', 'error')
            return redirect(url_for('edit_expense', expense_id=expense_id))
        except Exception as e:
            flash('An error occurred while updating the expense.', 'error')
            return redirect(url_for('edit_expense', expense_id=expense_id))
    
    categories = Category.query.all()
    return render_template('edit_expense.html', expense=expense, categories=categories, today=date.today())

@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    try:
        expense = Expense.query.get_or_404(expense_id)
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted successfully!', 'success')
    except Exception as e:
        flash('An error occurred while deleting the expense.', 'error')
    
    return redirect(url_for('expenses'))

@app.route('/reports')
def reports():
    total_spent = db.session.query(func.sum(Expense.amount)).scalar() or 0
    
    category_summary = db.session.query(
        Category.name,
        func.sum(Expense.amount).label('total')
    ).join(Expense).group_by(Category.id, Category.name).all()
    
    monthly_summary = db.session.query(
        extract('year', Expense.date).label('year'),
        extract('month', Expense.date).label('month'),
        func.sum(Expense.amount).label('total')
    ).group_by(
        extract('year', Expense.date),
        extract('month', Expense.date)
    ).order_by('year', 'month').all()
    
    recent_expenses = Expense.query.order_by(Expense.date.desc()).limit(5).all()
    
    return render_template('reports.html',
                         total_spent=total_spent,
                         category_summary=category_summary,
                         monthly_summary=monthly_summary,
                         recent_expenses=recent_expenses)

@app.route('/api/expenses')
def api_expenses():
    category_filter = request.args.get('category')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    query = Expense.query
    
    if category_filter and category_filter != 'all':
        query = query.filter(Expense.category_id == category_filter)
    
    if date_from:
        query = query.filter(Expense.date >= datetime.strptime(date_from, '%Y-%m-%d').date())
    
    if date_to:
        query = query.filter(Expense.date <= datetime.strptime(date_to, '%Y-%m-%d').date())
    
    expenses = query.order_by(Expense.date.desc()).all()
    return jsonify([expense.to_dict() for expense in expenses])

@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        try:
            name = request.form['name'].strip().title()
            description = request.form.get('description', '').strip()
            
            if not name:
                flash('Category name is required', 'error')
                return redirect(url_for('add_category'))
            
            existing_category = Category.query.filter_by(name=name).first()
            if existing_category:
                flash('Category already exists', 'error')
                return redirect(url_for('add_category'))
            
            category = Category(name=name, description=description)
            db.session.add(category)
            db.session.commit()
            flash('Category added successfully!', 'success')
            return redirect(url_for('categories'))
            
        except Exception as e:
            flash('An error occurred while adding the category.', 'error')
            return redirect(url_for('add_category'))
    
    return render_template('add_category.html')

@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    try:
        category = Category.query.get_or_404(category_id)
        
        if category.expenses:
            flash('Cannot delete category with existing expenses. Move or delete expenses first.', 'error')
            return redirect(url_for('categories'))
        
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
    except Exception as e:
        flash('An error occurred while deleting the category.', 'error')
    
    return redirect(url_for('categories'))

def init_db():
    with app.app_context():
        db.create_all()
        
        if not Category.query.first():
            default_categories = [
                Category(name='Food & Dining', description='Restaurants, groceries, and food delivery'),
                Category(name='Transportation', description='Gas, public transport, ride-sharing'),
                Category(name='Shopping', description='Clothing, electronics, general shopping'),
                Category(name='Bills & Utilities', description='Electricity, water, internet, phone bills'),
                Category(name='Entertainment', description='Movies, games, subscriptions'),
                Category(name='Healthcare', description='Medical expenses, pharmacy, insurance'),
                Category(name='Travel', description='Hotels, flights, vacation expenses'),
                Category(name='Education', description='Books, courses, educational materials'),
                Category(name='Other', description='Miscellaneous expenses')
            ]
            
            for category in default_categories:
                db.session.add(category)
            
            db.session.commit()
            print("Database initialized with default categories!")

@app.route('/download_dashboard_pdf')
def download_dashboard_pdf():
    """Generate and download PDF report of current dashboard view"""
    try:
        # Get the same filter parameters as the main dashboard
        date_filter = request.args.get('date', type=str)
        date_from = request.args.get('date_from', type=str)
        date_to = request.args.get('date_to', type=str)
        category_filter = request.args.get('category', type=int)
        selected_categories = request.args.getlist('categories', type=int)
        date_toggle = request.args.get('date_toggle', type=str) == 'on'
        date_range_mode = request.args.get('date_range_mode', type=str) == 'on'
        category_toggle = request.args.get('category_toggle', type=str) == 'on'
        
        # Get dashboard statistics based on current filters (same logic as index route)
        filtered_query = Expense.query
        
        # Apply category filter only if category toggle is ON
        if category_toggle:
            if selected_categories:
                filtered_query = filtered_query.filter(Expense.category_id.in_(selected_categories))
            elif category_filter:
                filtered_query = filtered_query.filter(Expense.category_id == category_filter)
        
        # Apply date filter if toggle is ON
        if date_toggle:
            if date_range_mode and date_from and date_to:
                try:
                    from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
                    to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
                    filtered_query = filtered_query.filter(
                        Expense.date >= from_date,
                        Expense.date <= to_date
                    )
                except ValueError:
                    pass
            elif date_filter:
                try:
                    filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                    filtered_query = filtered_query.filter(Expense.date == filter_date)
                except ValueError:
                    pass
        
        # Calculate filtered totals
        total_spent = db.session.query(func.sum(Expense.amount)).filter(
            Expense.id.in_(filtered_query.with_entities(Expense.id))
        ).scalar() or 0
        
        # For monthly expenses, show filtered total or current month
        if date_toggle and (date_filter or (date_range_mode and date_from and date_to)):
            month_spent = total_spent
        else:
            current_month = datetime.now().month
            current_year = datetime.now().year
            month_query = db.session.query(func.sum(Expense.amount)).filter(
                extract('year', Expense.date) == current_year,
                extract('month', Expense.date) == current_month
            )
            if category_toggle:
                if selected_categories:
                    month_query = month_query.filter(Expense.category_id.in_(selected_categories))
                elif category_filter:
                    month_query = month_query.filter(Expense.category_id == category_filter)
            month_spent = month_query.scalar() or 0
        
        total_expenses = filtered_query.count()
        
        # Get recent expenses with filtering
        recent_query = Expense.query
        
        # Apply date filter - only if toggle is ON
        if date_toggle:
            if date_range_mode and date_from and date_to:
                try:
                    from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
                    to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
                    recent_query = recent_query.filter(
                        Expense.date >= from_date,
                        Expense.date <= to_date
                    )
                except ValueError:
                    pass
            elif date_filter:
                try:
                    filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                    recent_query = recent_query.filter(Expense.date == filter_date)
                except ValueError:
                    pass
        
        # Apply category filter only if category toggle is ON
        if category_toggle:
            if selected_categories:
                recent_query = recent_query.filter(Expense.category_id.in_(selected_categories))
            elif category_filter:
                recent_query = recent_query.filter(Expense.category_id == category_filter)
        
        recent_expenses = recent_query.order_by(Expense.date.desc()).limit(10).all()
        
        # Get all categories for filter display
        categories = Category.query.all()
        
        # Create PDF using ReportLab
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#007bff'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#007bff'),
            alignment=TA_LEFT,
            spaceAfter=12
        )
        
        # Build PDF content
        story = []
        
        # Title
        story.append(Paragraph("📊 Personal Expense Tracker - Dashboard Report", title_style))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Filter Information
        if date_toggle or category_toggle:
            filter_text = "🔍 Applied Filters:<br/>"
            if date_toggle:
                if date_range_mode and date_from and date_to:
                    filter_text += f"<b>Date Range:</b> {date_from} to {date_to}<br/>"
                elif date_filter:
                    filter_text += f"<b>Date:</b> {date_filter}<br/>"
            if category_toggle:
                if selected_categories:
                    filter_text += f"<b>Categories:</b> {len(selected_categories)} categories selected<br/>"
                elif selected_category:
                    category_name = next((cat.name for cat in categories if cat.id == category_filter), 'Unknown')
                    filter_text += f"<b>Category:</b> {category_name}<br/>"
            if not date_toggle and not category_toggle:
                filter_text += "<b>No filters applied</b> - Showing all expenses<br/>"
            
            story.append(Paragraph(filter_text, styles['Normal']))
            story.append(Spacer(1, 15))
        
        # Dashboard Statistics
        story.append(Paragraph("Dashboard Statistics", subtitle_style))
        
        # Create stats table
        stats_data = [
            ['Metric', 'Value', 'Description'],
            ['Total Spent', f'${total_spent:.2f}', 'Total amount spent'],
            ['Monthly/Date Range', f'${month_spent:.2f}', 'Monthly or filtered total'],
            ['Total Expenses', str(total_expenses), 'Number of transactions']
        ]
        
        stats_table = Table(stats_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 20))
        
        # Recent Expenses
        story.append(Paragraph("Recent Expenses", subtitle_style))
        
        if recent_expenses:
            # Create expenses table
            expenses_data = [['Date', 'Description', 'Category', 'Amount', 'Type']]
            for expense in recent_expenses:
                expense_type = 'Monthly' if expense.is_monthly else 'One-time'
                expenses_data.append([
                    expense.date.strftime('%Y-%m-%d'),
                    expense.description,
                    expense.category.name,
                    f'${expense.amount:.2f}',
                    expense_type
                ])
            
            expenses_table = Table(expenses_data, colWidths=[1*inch, 2.5*inch, 1*inch, 1*inch, 0.8*inch])
            expenses_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            story.append(expenses_table)
        else:
            story.append(Paragraph("No expenses found matching the current filters.", styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Summary
        story.append(Paragraph("Summary", subtitle_style))
        summary_data = [
            ['Metric', 'Value'],
            ['Total Transactions', str(total_expenses)],
            ['Average per Expense', f'${(total_spent / total_expenses):.2f}' if total_expenses > 0 else '$0.00'],
            ['Available Categories', str(len(categories))]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("This report was generated by Personal Expense Tracker", styles['Normal']))
        story.append(Paragraph("Report includes all data based on applied filters at the time of generation", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF content
        pdf_content = buffer.getvalue()
        buffer.close()
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'expense_dashboard_report_{timestamp}.pdf'
        
        # Return PDF as download
        return Response(
            pdf_content,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename={filename}',
                'Content-Type': 'application/pdf'
            }
        )
        
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
